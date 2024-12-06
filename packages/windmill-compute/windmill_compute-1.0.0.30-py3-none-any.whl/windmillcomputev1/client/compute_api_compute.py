#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/15 15:54
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : compute_api_compute.py
# @Software: PyCharm
"""
import re
from typing import Optional

compute_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/computes/(?P<local_name>.+?)$")


class ComputeName:
    """
    The name of pipeline.
    """
    def __init__(self, workspace_id: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.local_name = local_name


def parse_compute_name(name: str) -> Optional[ComputeName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    if name is None:
        return None
    m = compute_name_regex.match(name)
    if m is None:
        return None
    return ComputeName(m.group("workspace_id"), m.group("local_name"))