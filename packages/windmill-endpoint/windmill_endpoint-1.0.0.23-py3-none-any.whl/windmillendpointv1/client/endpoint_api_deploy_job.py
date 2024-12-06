# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/15 14:31
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : endpoint_api_deploy_job.py
# @Software: PyCharm
"""
import re
from typing import Optional, Dict
from windmillmodelv1.client.model_api_model import PreferModelServerParameters

deploy_endpoint_job_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/endpointhubs/(?P<endpoint_hub_name>.+?)/jobs/(?P<local_name>.+?)$")


class DeployEndpointJobName:
    """
    Deploy endpoint job name.
    """
    def __init__(self, workspace_id: str = None, endpoint_hub_name: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.endpoint_hub_name = endpoint_hub_name
        self.local_name = local_name


def parse_deploy_endpoint_job_name(name: str) -> Optional[DeployEndpointJobName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    m = deploy_endpoint_job_name_regex.match(name)
    if m is None:
        return None
    return DeployEndpointJobName(m.group("workspace_id"), m.group("endpoint_hub_name"), m.group("local_name"))


def get_template_parameters(model_server_parameters: Optional[PreferModelServerParameters]) -> Dict[str, str]:
    """
    Get template parameters.
    :param model_server_parameters:
    :return:
    """
    template_parameters = {}

    if model_server_parameters is not None:
        if model_server_parameters.image:
            template_parameters["image.imageName"] = model_server_parameters.image
        if model_server_parameters.resource.accelerator:
            template_parameters["resource.accelerator"] = model_server_parameters.resource.accelerator
        if model_server_parameters.resource.gpu:
            template_parameters["resource.gpu"] = model_server_parameters.resource.gpu
        if model_server_parameters.resource.limits.cpu:
            template_parameters["resource.limits.cpu"] = model_server_parameters.resource.limits.cpu
        if model_server_parameters.resource.limits.mem:
            template_parameters["resource.limits.mem"] = model_server_parameters.resource.limits.mem
        if model_server_parameters.resource.requests.cpu:
            template_parameters["resource.requests.cpu"] = model_server_parameters.resource.requests.cpu
        if model_server_parameters.resource.requests.mem:
            template_parameters["resource.requests.mem"] = model_server_parameters.resource.requests.mem
        if model_server_parameters.qps != 0.0:
            template_parameters["hpa.averageValue"] = f"{model_server_parameters.qps:.1f}"

        if model_server_parameters.env:
            for k, v in model_server_parameters.env.items():
                template_parameters[f"env.{k}"] = v

        if model_server_parameters.args:
            for k, v in model_server_parameters.args.items():
                template_parameters[f"args.{k}"] = v

    return template_parameters
