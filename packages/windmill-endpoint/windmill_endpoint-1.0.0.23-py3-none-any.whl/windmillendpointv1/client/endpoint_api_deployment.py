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
from typing import Optional
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name, parse_artifact
from windmillcategoryv1.client.category_api import split_category
deployment_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/endpointhubs/"
               "(?P<endpoint_hub_name>.+?)/deployments/(?P<local_name>.+?)$")


class DeploymentName:
    """
    Deployment name.
    """
    def __init__(self, workspace_id: str = None, endpoint_hub_name: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.endpoint_hub_name = endpoint_hub_name
        self.local_name = local_name


def parse_deployment_name(name: str) -> Optional[DeploymentName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    m = deployment_name_regex.match(name)
    if m is None:
        return None
    return DeploymentName(m.group("workspace_id"), m.group("endpoint_hub_name"), m.group("local_name"))


def get_deployment_name(accelerator: str, deployments: dict = {}, server_kind: str = "Triton") -> str:
    """
    Get deployment name.
    :param accelerator:
    :param deployments:
    :param server_kind:
    :return:
    """
    default_deployment_prefix = "workspaces/public/endpointhubs/default/deployments/" + server_kind.lower() + "-"
    accelerator = get_accelerator(accelerator)
    deployment_name = deployments.get(accelerator)
    if deployment_name == "":
        deployment_name = default_deployment_prefix + accelerator
    artiafact_name = parse_artifact_name(deployment_name)
    if artiafact_name.version == "" or artiafact_name.version is None:
        deployment_name = artiafact_name.object_name + "/versions/latest"
    return deployment_name


def get_accelerator(accelerator: str) -> str:
    """
    Get accelerator name.
    :param accelerator:
    :return:
    """
    levels = split_category(accelerator)

    if len(levels) > 1:
        return levels[0].lower()

    if accelerator in ["K200", "R200", "R480"]:
        return "kunlun"

    if "Ascend" in accelerator or "Atlas" in accelerator:
        return "ascend"

    return "nvidia"