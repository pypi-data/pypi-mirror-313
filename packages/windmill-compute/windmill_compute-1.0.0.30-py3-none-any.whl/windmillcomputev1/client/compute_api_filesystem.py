#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/4/17 20:32
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : compute_api_filesystem.py
# @Software: PyCharm
"""
import re
from typing import Optional

fs_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/filesystems/(?P<local_name>.+?)$")


class FilesystemName:
    """
    The name of pipeline.
    """
    def __init__(self, workspace_id: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.local_name = local_name


def parse_filesystem_name(name: str) -> Optional[FilesystemName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    m = fs_name_regex.match(name)
    if m is None:
        return None
    return FilesystemName(m.group("workspace_id"), m.group("local_name"))