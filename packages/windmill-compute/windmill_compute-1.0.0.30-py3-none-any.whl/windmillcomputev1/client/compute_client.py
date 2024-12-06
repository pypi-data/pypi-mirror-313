#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/25 15:45
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : compute_client.py
# @Software: PyCharm
"""
import os
from typing import Optional, List, Callable
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.bce_client_configuration import BceClientConfiguration
import json
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest
from ..filesystem import blobstore
from ..filesystem.blobstore import blobstore_config


class ComputeClient(BceInternalClient):
    """
    A client class for interacting with the compute service. Initializes with default configuration.

    This client provides an interface to interact with the compute service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving compute within a specified workspace.

    """

    def get_filesystem(self, workspace_id: str, local_name: str):
        """
        Gets a filesystem object from specified workspace.
        :param workspace_id: 工作区id
        :param local_name: filesystem name
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/filesystems/" + local_name,
                                             encoding="utf-8"))

    def get_filesystem_credential(self, workspace_id: str, local_name: str):
        """
        Gets a filesystem object contain credential from specified workspace.
        :param workspace_id: 工作区id
        :param local_name: filesystem name
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes(
                                      "/v1/workspaces/" + workspace_id + "/filesystems/" + local_name + "/credentials",
                                      encoding="utf-8"))

    def suggest_filesystem(self, workspace_id: str,
                           guest_name: str,
                           tips: Optional[str] = [],
                           exclude_credentials: Optional[bool] = False):
        """
        Suggests filesystems for specified guest name.
        :param workspace_id: 工作区 id
        :param guest_name: 资源名称
        :param tips:
        :param exclude_credentials: 是否隐藏密钥信息
        :return:
        """
        body = {
            "workspaceID": workspace_id,
            "guestName": guest_name,
            "tips": tips,
            "excludeCredentials": exclude_credentials
        }

        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/filesystems/suggest",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def build_base_uri(self, filesystem: Callable):
        """
        Build base uri from filesystem.

        Args:
            filesystem: (Callable): filesystem
        """
        return filesystem["kind"] + "://" + filesystem["endpoint"]

    def suggest_first_filesystem(self, workspace_id: str,
                                 guest_name: str,
                                 tips: Optional[str] = [],
                                 exclude_credentials: Optional[bool] = False):
        """
        Suggests first filesystem for specified guest name.

        Args:
            workspace_id (str): workspace id
            guest_name (str): guest name
            tips(list, optional): tips
            exclude_credentials(str, optional): 是否隐藏密钥信息
        """
        resp = self.suggest_filesystem(workspace_id=workspace_id,
                                       guest_name=guest_name,
                                       tips=tips,
                                       exclude_credentials=exclude_credentials)
        assert len(resp.fileSystems) > 0, "Suggest response {} filesystem length is zero, " \
                                          "please check your workspace id: {} and guest name: {}".format(resp,
                                                                                                         workspace_id,
                                                                                                         guest_name)
        return self._first(resp.fileSystems)

    def get_compute(self, workspace_id: str, local_name: str):
        """
        Gets compute object from specified workspace.
        :param workspace_id:
        :param local_name:
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/computes/" + local_name,
                                             encoding="utf-8"))

    def get_compute_credential(self, workspace_id: str, local_name: str, output_path: str = ""):
        """
        Gets compute object from specified workspace contain credential.
        :param workspace_id:
        :param local_name:
        :param output_path:
        :return:
        """
        resp = self._send_request(http_method=http_methods.GET,
                                  path=bytes(
                                      "/v1/workspaces/" + workspace_id + "/computes/" + local_name + "/credentials",
                                      encoding="utf-8"))
        if output_path != "":
            kube_config = resp.config.get("kubeConfig")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(kube_config)
        return resp

    def suggest_compute(self,
                        workspace_id: str,
                        guest_name: str,
                        tips: Optional[str] = None,
                        exclude_credentials: Optional[bool] = False):
        """
        Suggests compute for specified guest name.
        :param workspace_id: 工作区 id
        :param guest_name: 资源名称
        :param tips:
        :param exclude_credentials: 是否隐藏密钥信息
        :return:
        """
        if tips is None:
            tips = []
        body = {
            "workspaceID": workspace_id,
            "guestName": guest_name,
            "tips": tips,
            "excludeCredentials": exclude_credentials
        }

        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/computes/suggest",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def suggest_first_compute(self, workspace_id: str,
                              guest_name: str,
                              tips: Optional[str] = [],
                              exclude_credentials: Optional[bool] = False):
        """
        Suggests first compute for specified guest name.

        Args:
            workspace_id (str): workspace id
            guest_name (str): guest name
            tips(list, optional): tips
            exclude_credentials(str, optional): 是否隐藏密钥信息
        """
        resp = self.suggest_compute(workspace_id=workspace_id,
                                    guest_name=guest_name,
                                    tips=tips,
                                    exclude_credentials=exclude_credentials)
        assert len(resp.computes) > 0, "Suggest response {} computes length is zero, " \
                                       "please check your workspace id: {} and guest name: {}".format(resp,
                                                                                                      workspace_id,
                                                                                                      guest_name)
        return self._first(resp.computes)

    def list_compute(self, workspace_id: str, parent_name: Optional[str] = "", kind: Optional[str] = "",
                     host: Optional[str] = "", namespace: Optional[str] = "",
                     filter_param: Optional[str] = "",
                     page_request: Optional[PagingRequest] = PagingRequest()):
        """
        Lists model stores in the system.
        Args:
            workspace_id (str): 工作区 id
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
            parent_name (str, optional):
            kind (str, optional):
            host (str, optional):
            namespace (str, optional):

        Returns:
            HTTP request response
        """
        params = {
            "filter": filter_param,
            "parentName": parent_name,
            "kind": kind,
            "namespace": namespace,
            "host": host,
            "pageNo": str(page_request.get_page_no()),
            "pageSize": str(page_request.get_page_size()),
            "order": page_request.order,
            "orderBy": page_request.orderby}
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/computes", encoding="utf-8"),
                                  params=params)

    def get_blobstore(self, workspace_id: str, guest_name: str, tips: Optional[str] = [],
                      exclude_credentials: Optional[bool] = False):
        """
        get blobstore client by guest_name
        Args:
            workspace_id (str): workspace id
            guest_name (str): guest name
            tips(list, optional): tips
            exclude_credentials(str, optional): 是否隐藏密钥信息

        Returns:
            blobstore client
        """
        filesystem = self.suggest_first_filesystem(workspace_id,
                                                   guest_name,
                                                   tips,
                                                   exclude_credentials)
        return blobstore(filesystem=filesystem)

    @staticmethod
    def _first(values: List):
        assert len(values) > 0, "empty list"
        return values[0]

    def list_flavour(self,
                     cluster_name: Optional[str] = "",
                     name: Optional[str] = "",
                     marker: Optional[str] = "",
                     max_keys: Optional[str] = ""):
        """
        list_flavour
        Args:

        Returns:
            http request response
        """
        params = {"name": name,
                  "marker": marker,
                  "maxKeys": max_keys}
        if cluster_name:
            params["clusterName"] = cluster_name
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/flavours", encoding="utf-8"),
                                  params=params)

    def get_flavour(self, name: str):
        """
        Gets compute object from specified workspace.
        :param name:
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/flavours/" + name,
                                             encoding="utf-8"))