#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/9/10
# @Author  : zhangzhijun
# @File    : download_kubeconfig.py
"""
import os
from argparse import ArgumentParser

from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.client.compute_api_compute import parse_compute_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--compute-name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()

    return args


def run():
    """
    download kubeconfig.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    name = parse_compute_name(args.compute_name)
    windmill_client.get_compute_credential(workspace_id=name.workspace_id,
                                           local_name=name.local_name,
                                           output_path="/root/.kube/config")


if __name__ == "__main__":
    run()
