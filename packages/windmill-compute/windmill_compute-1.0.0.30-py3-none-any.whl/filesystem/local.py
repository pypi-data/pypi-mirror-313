#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/10/24 17:02
# @Author : dongling01@baidu.com
# @File : local.py
# @Software: PyCharm
"""
from typing import Dict
from urllib.parse import urlparse
import os
import errno
import datetime

from .blobstore import BlobStore, BlobMeta

KIND_LOCAL = "file"


class LocalBlobStore(BlobStore):
    """
    A client class for local blobstore.

    Args:
        endpoint: blobstore endpoint.
        config: blobstore config.
    """

    def __init__(self, endpoint: str, config: Dict):
        super(LocalBlobStore, self).__init__(endpoint, config)

        if not os.path.isdir(endpoint):
            raise ValueError(f"basePath: {endpoint} must be a directory")

        self.base_path = os.path.abspath(endpoint)

    def _get_full_path(self, path):
        """
        get full path
        """
        parsed_url = urlparse(path)

        if parsed_url.scheme == '':
            if not os.path.isabs(path):
                return os.path.join(self.base_path, path)
        elif parsed_url.scheme == KIND_LOCAL:
            path = parsed_url.netloc + parsed_url.path
            if not os.path.isabs(path):
                path = "/" + path
        else:
            raise ValueError("scheme should be empty or 'file'")

        if not path.startswith(self.base_path):
            raise ValueError(f"path {path} does not begin with basePath {self.base_path}")

        return path

    def read_raw(self, path):
        """
        read data
        """
        full_path = self._get_full_path(path)
        try:
            with open(full_path, 'rb') as file:
                return file.read()
        except OSError as e:
            raise e

    def write_raw(self, path: str, content_type: str, data):
        """
        write data
        """
        full_path = self._get_full_path(path)

        if isinstance(data, str):
            data = data.encode('utf-8')

        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as file:
                file.write(data)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

    def list_meta(self, path):
        """
        list meta
        """
        full_path = self._get_full_path(path)
        if not os.path.isdir(full_path):
            raise ValueError("list meta must operate a dir")

        metas = []
        metas = self._add_file_metas(path, full_path, metas, True)
        return metas


    def _add_file_metas(self, path, full_path, metas, recursive):
        """
        add file metas
        """
        try:
            entries = os.listdir(full_path)
        except OSError as e:
            return metas, e

        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            if os.path.isdir(entry_path):
                if recursive:
                    metas = self._add_file_metas(os.path.join(path, entry), entry_path, metas, recursive)
                continue
            info = os.stat(entry_path)
            metas.append(BlobMeta(
                name=os.path.join(path, entry),
                size=info.st_size,
                url_path=entry_path,
                last_modified=datetime.datetime.fromtimestamp(info.st_mtime)
            ))
        return metas

    def upload_file(self, file_name: str, path: str):
        """
        upload file
        """
        pass

    def download_file(self, path: str, file_name: str):
        """
        download file
        """
        pass



