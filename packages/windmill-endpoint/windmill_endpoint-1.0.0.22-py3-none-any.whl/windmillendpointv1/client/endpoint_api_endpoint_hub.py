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
from typing import Optional, List
from pydantic import BaseModel, Field


endpoint_hub_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/endpointhubs/(?P<local_name>.+?)$")


class EndpointHubName:
    """
    Deploy endpoint job name.
    """
    def __init__(self, workspace_id: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.local_name = local_name


def parse_endpoint_hub_name(name: str) -> Optional[EndpointHubName]:
    """
    Get endpoint hub name
    """
    m = endpoint_hub_name_regex.match(name)
    if m is None:
        return None
    return EndpointHubName(m.group("workspace_id"), m.group("local_name"))


class CreateEndpointHubRequest(BaseModel):
    """
    Create endpoint hub request.
    """
    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    display_name: Optional[str] = Field(None, alias="displayName")
    description: Optional[str] = None
    filesystem_name: Optional[str] = Field(None, alias="fileSystemName")
    compute_name: Optional[str] = Field(None, alias="computeName")
