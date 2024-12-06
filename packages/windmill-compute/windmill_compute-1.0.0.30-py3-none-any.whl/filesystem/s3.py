#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/9/5 17:02
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : blobstore.py
# @Software: PyCharm
"""
from typing import Dict
from urllib.parse import urlparse
import boto3
import botocore
import os
from .blobstore import BlobStore, BlobMeta
from .blobstore import CONFIG_AK, CONFIG_SK, CONFIG_REGION, CONFIG_HOST, KIND_S3, CONFIG_DISABLE_SSL


def remove_prefix(uri, prefix):
    """
    Remove prefix from uri.
    """
    return uri[len(prefix):] if uri.startswith(prefix) else uri


class S3BlobStore(BlobStore):
    """
    A client class for s3 blobstore.

    Args:
        endpoint: blobstore endpoint.
        config: blobstore config.
    """

    def __init__(self, endpoint: str, config: Dict):
        super(S3BlobStore, self).__init__(endpoint, config)

        access_key_id = self.config[CONFIG_AK]
        secret_access_key = self.config[CONFIG_SK]
        region = self.config[CONFIG_REGION]
        endpoint_url = self.config[CONFIG_HOST]

        assert CONFIG_DISABLE_SSL in config, "{} should be set in {}".format(CONFIG_DISABLE_SSL, config)
        if not endpoint_url.startswith("http"):
            if config[CONFIG_DISABLE_SSL] != "false":
                endpoint_url = "http://" + endpoint_url
            else:
                endpoint_url = "https://" + endpoint_url

        self._bucket = endpoint.split("/")[0]

        self._client = boto3.client(
            "s3", aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key, endpoint_url=endpoint_url, region_name=region)

    def _get_bucket_and_key(self, path: str):
        parse_endpoint = urlparse(path)
        if parse_endpoint.scheme == "":
            return self._bucket, path.lstrip('/')

        assert parse_endpoint.scheme == KIND_S3, "Path scheme should be {}, bug got is {}".format(KIND_S3,
                                                                                                  parse_endpoint.scheme)
        bucket = parse_endpoint.netloc
        bucket_index = path.find(bucket)
        return bucket, path[bucket_index + len(bucket):].lstrip('/')

    @staticmethod
    def _fetch_path(path: str):
        if os.path.splitext(path)[1] == "":
            path = path.rstrip("/") + "/"

        return path

    def read_raw(self, path: str):
        bucket, key = self._get_bucket_and_key(path)
        response = self._client.get_object(Bucket=bucket, Key=key)

        return response["Body"].read()

    def list_meta(self, path: str):
        path = self._fetch_path(path)
        bucket, key = self._get_bucket_and_key(path)
        response = self._client.list_objects_v2(Bucket=bucket, Prefix=key)

        metas = []
        for obj in response.get('Contents', []):
            if os.path.splitext(obj['Key'])[1] != "":
                metas.append(BlobMeta(
                    name=remove_prefix(obj["Key"], response["Prefix"]),
                    size=obj["Size"],
                    url_path=KIND_S3 + "://" + bucket + "/" + obj["Key"],
                    last_modified=obj["LastModified"],
                ))

        return metas

    def write_raw(self, path: str, content_type: str, data):
        bucket, key = self._get_bucket_and_key(path)
        # ContentType value is: image/png, image/jpeg, application/json, text/plain...
        self._client.put_object(Bucket=bucket, Body=data, Key=key, ContentType=content_type)

    def upload_file(self, file_name: str, path: str):
        assert path.startswith("s3://"), "Path should start with s3://, but got {}".format(path)
        bucket, key = self._get_bucket_and_key(path)
        self._client.upload_file(Filename=file_name, Bucket=bucket, Key=key)

    def download_file(self, path: str, file_name: str):
        bucket, key = self._get_bucket_and_key(path)
        self._client.download_file(Bucket=bucket, Key=key, Filename=file_name)

    def head_object(self, path: str):
        """
        Check if the object exists.
        :param path:
        :return:
        """
        bucket, key = self._get_bucket_and_key(path)
        try:
            resp = self._client.head_object(Bucket=bucket, Key=key)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
