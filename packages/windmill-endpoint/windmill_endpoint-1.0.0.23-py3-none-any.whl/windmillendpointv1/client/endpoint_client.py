# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/9/15 14:13
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : endpoint_client.py
# @Software: PyCharm
"""
import json
from multidict import MultiDict
from typing import Optional
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import http_content_types
from .endpoint_api_endpoint_hub import CreateEndpointHubRequest
from .endpoint_api import CreateEndpointRequest


class EndpointClient(BceInternalClient):
    """
    A client class for interacting with the endpoint service. Initializes with default configuration.

    This client provides an interface to interact with the endpoint service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving endpoint within a specified workspace.

    """

    def create_endpoint(self,
                        req: CreateEndpointRequest):
        """
        Creates new endpoint

        Args:
            req
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/"
                                             + req.workspace_id
                                             + "/endpointhubs/"
                                             + req.endpoint_hub_name +
                                             "/endpoints",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=req.json(by_alias=True))

    def list_endpoint(self, workspace_id: str, endpoint_hub_name: str, kind: Optional[str] = "",
                      category: Optional[str] = "", tags: Optional[str] = "",
                      filter_param: Optional[str] = "", page_request: Optional[PagingRequest] = PagingRequest()):
        """

        Lists endpoint in the system.

        Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 端点中心名称
            kind: 类型
            category (str, optional): 按类别筛选
            tags (str, optional): 按版本标签筛选
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
        Returns:
            HTTP request response
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", filter_param)
        params.add("kind", str(kind))
        if category:
            for i in category:
                params.add("categories", i)
        if tags:
            for i in tags:
                params.add("tags", i)
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/endpoints", encoding="utf-8"),
                                  params=params)

    def get_endpoint(self, workspace_id: str, endpoint_hub_name: str, local_name: str):
        """
        get endpoint in the system.

        Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 端点中心名称
            local_name: 名称
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/endpoints/"
                                             + local_name, encoding="utf-8"))

    """
    deploy_endpoint_job api
    """

    def get_deploy_endpoint_job(self, workspace_id: str, endpoint_hub_name: str, local_name: str):
        """
        get deploy endpoint job

        Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 端点中心名称
            local_name: 名称
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/jobs/" + local_name,
                                             encoding="utf-8"))

    def list_deployment(self, workspace_id: str,
                        endpoint_hub_name: str,
                        f: Optional[str] = "",
                        server_kind: Optional[str] = "",
                        spec_kind: Optional[str] = "",
                        page_request: Optional[PagingRequest] = PagingRequest()):
        """

        :param page_request:
        :param spec_kind:
        :param server_kind:
        :param f:
        :param workspace_id:
        :param endpoint_hub_name:
        :return:
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", f)
        params.add("specKind", str(spec_kind))

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name +
                                             "/deployments", encoding="utf-8"),
                                  params=params)

    """
    endpoint_hub_api
    """

    def create_endpoint_hub(self,
                            req: CreateEndpointHubRequest):
        """
        create endpoint hub
        :param req
        :return:
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + req.workspace_id
                + "/endpointhubs",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=req.json(by_alias=True),
        )

    def list_endpoint_hub(self, workspace_id: str,
                          f: Optional[str] = "",
                          page_request: Optional[PagingRequest] = PagingRequest()):
        """
        Lists endpoint hub in the system.
        Args:
            workspace_id (str): 工作区 id
            f (str): 过滤参数
            page_request: 分页参数
        Returns:
            HTTP request response
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", f)

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs", encoding="utf-8"),
                                  params=params)

    def get_endpoint_hub(self, workspace_id: str, local_name: str):
        """
        get endpoint hub in the system.
        Args:
            workspace_id (str): 工作区 id
            local_name(str): 名称
        Returns:
            HTTP request response
        """

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + local_name, encoding="utf-8"))

    """
    deployment api
    """

    def get_deployment(self, workspace_id: str, endpoint_hub_name: str, local_name: str):
        """
        get deployment in the system.
         Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 端点中心名称
            local_name: 名称
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/deployments/" + local_name,
                                             encoding="utf-8"))

    def create_deploy_endpoint_job(
            self,
            workspace_id: str,
            endpoint_hub_name: str,
            kind: str,
            endpoint_name: str,
            local_name: Optional[str] = "",
            display_name: Optional[str] = "",
            description: Optional[str] = "",
            policy: Optional[str] = None,
            resource_tips: Optional[dict] = None,
            job_compute_name: Optional[str] = "",
            job_compute: Optional[dict] = None,
            job_spec_raw: Optional[str] = "",
            endpoint_kind: Optional[str] = "",
            endpoint_compute_name: Optional[str] = "",
            endpoint_compute: Optional[dict] = None,
            endpoint_uri: Optional[str] = "",
            model_name: Optional[str] = "",
            model_uri: Optional[str] = "",
            model_server_kind: Optional[str] = "",
            spec_kind: Optional[str] = "",
            spec_name: Optional[str] = "",
            spec_uri: Optional[str] = "",
            spec_filesystem: Optional[dict] = None,
            dataset_name: Optional[str] = "",
            dataset_uri: Optional[str] = "",
            dataset_filesystem: Optional[dict] = None,
            artifact_name: Optional[str] = "",
            artifact_uri: Optional[str] = "",
            artifact_filesystem: Optional[dict] = None,
            server_kind: Optional[str] = "",
            template_parameters: Optional[dict] = None,
            pipeline_parameters: Optional[dict] = None,

    ):
        """
        create_deploy_endpoint_job
        :param workspace_id:
        :param endpoint_hub_name:
        :param local_name:
        :param kind:
        :param policy:
        :param endpoint_name:
        :param display_name:
        :param description:
        :param resource_tips:
        :param job_compute_name:
        :param job_compute:
        :param job_spec_raw:
        :param endpoint_kind:
        :param endpoint_compute_name:
        :param endpoint_compute:
        :param endpoint_uri:
        :param model_name:
        :param model_uri:
        :param model_server_kind:
        :param spec_kind:
        :param spec_name:
        :param spec_uri:
        :param spec_filesystem:
        :param dataset_name:
        :param dataset_uri:
        :param dataset_filesystem:
        :param artifact_name:
        :param artifact_uri:
        :param artifact_filesystem:
        :param server_kind:
        :param template_parameters:
        :param pipeline_parameters:
        :return:
        """
        body = {
            "workspaceID": workspace_id,
            "endpointHubName": endpoint_hub_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "resourceTips": resource_tips,
            "kind": kind,
            "policy": policy,
            "jobComputeName": job_compute_name,
            "jobCompute": job_compute,
            "jobSpecRaw": job_spec_raw,
            "endpointKind": endpoint_kind,
            "endpointName": endpoint_name,
            "endpointComputeName": endpoint_compute_name,
            "endpointCompute": endpoint_compute,
            "endpointUri": endpoint_uri,
            "modelName": model_name,
            "modelUri": model_uri,
            "modelServerKind": model_server_kind,
            "specKind": spec_kind,
            "specName": spec_name,
            "specUri": spec_uri,
            "specFilesystem": spec_filesystem,
            "datasetName": dataset_name,
            "datasetUri": dataset_uri,
            "datasetFilesystem": dataset_filesystem,
            "artifactName": artifact_name,
            "artifactUri": artifact_uri,
            "artifactFilesystem": artifact_filesystem,
            "serverKind": server_kind,
            "templateParameters": template_parameters,
            "pipelineParameters": pipeline_parameters,
        }

        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/endpointhubs/"
                + endpoint_hub_name
                + "/jobs",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def update_endpoint(
            self,
            workspace_id: str,
            endpoint_hub_name: str,
            local_name: str,
            display_name: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[dict] = None,
            category: Optional[str] = None,
    ):
        """
        update endpoint
        :param workspace_id:
        :param endpoint_hub_name:
        :param local_name:
        :param display_name:
        :param description:
        :param tags:
        :param category:
        :return:
        """
        body = {
            "workspaceID": workspace_id,
            "endpointHubName": endpoint_hub_name,
            "endpointName": local_name,
            "displayName": display_name,
            "description": description,
            "tags": tags,
            "category": category,
        }
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/endpointhubs/"
                + endpoint_hub_name
                + "/endpoints/"
                + local_name,
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def list_deploy_endpoint_job(
            self,
            workspace_id: str,
            endpoint_hub_name: str,
            kind: Optional[str] = "",
            endpoint_name: Optional[str] = "",
            endpoint_kind: Optional[str] = "",
            filter_param: Optional[str] = "",
            model_name: Optional[str] = "",
            artifact_name: Optional[str] = "",
            spec_kind: Optional[str] = "",
            spec_name: Optional[str] = "",
            page_request: Optional[PagingRequest] = PagingRequest()
    ):
        """

        Lists deploy_endpoint_job in the system.

        Args:
            workspace_id (str): 工作区 id
            endpoint_hub_name (str): 服务中心名称
            kind: job类型
            endpoint_name: 服务名称
            endpoint_kind: 服务类型
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            model_name: 模型名称
            artifact_name: 模型版本名称
            spec_kind: 模板引擎类型
            spec_name: 部署配置deployment version name
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
        Returns:
            HTTP request response
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", filter_param)
        params.add("kind", str(kind))
        params.add("endpointKind", str(endpoint_kind))
        params.add("specKind", str(spec_kind))
        params.add("endpointName", str(endpoint_name))
        params.add("modelName", str(model_name))
        params.add("artifactName", str(artifact_name))
        params.add("specName", str(spec_name))

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/endpointhubs/" + endpoint_hub_name + "/jobs", encoding="utf-8"),
                                  params=params)