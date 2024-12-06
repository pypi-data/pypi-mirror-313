#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/1/22
# @Author  : yanxiaodong
# @File    : initialize.py
"""
from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel
from abc import ABCMeta, abstractmethod

KIND_S3 = "s3"

CONFIG_AK = "ak"
CONFIG_SK = "sk"
CONFIG_REGION = "region"
CONFIG_HOST = "host"
CONFIG_DISABLE_SSL = "disableSSL"


def blobstore_config(filesystem):
    """
    Set the blobstore config.
    """
    config = filesystem["config"]

    if config.get("ak") is None or config.get("sk") is None:
        config[CONFIG_AK] = filesystem["credential"]["accessKey"]
        config[CONFIG_SK] = filesystem["credential"]["secretKey"]
    config[CONFIG_HOST] = filesystem[CONFIG_HOST]

    return filesystem["kind"], filesystem["endpoint"], config


class BlobMeta(BaseModel):
    """
    Blob meta.
    """
    name: str
    content_type: str = ""
    size: int = 0
    url_path: str = ""
    last_modified: datetime


class BlobStore(metaclass=ABCMeta):
    """
    A client class for blobstore.

    Args:
        endpoint: blobstore endpoint.
        config: blobstore config.
    """
    def __init__(self, endpoint: str, config: Dict):
        self.endpoint = endpoint
        self.config = config

    @abstractmethod
    def list_meta(self, path: str) -> List[BlobMeta]:
        """
        List the blob meta.
        """
        pass

    @abstractmethod
    def read_raw(self, path: str):
        """
        Read the blob.
        """
        pass

    @abstractmethod
    def write_raw(self, path: str, content_type: str, data):
        """
        Write the blob.
        """
        pass

    @abstractmethod
    def upload_file(self, file_name: str, path: str):
        """
        Upload the file.
        """
        pass

    @abstractmethod
    def download_file(self, path: str, file_name: str):
        """
        Download the file.
        """
        pass
