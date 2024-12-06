# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
getter for kubernetes resource status
"""
import argparse
import datetime
import json

from kubernetes import client, config
from pydantic import BaseModel


class DeploymentCondition(BaseModel):
    type: str = ""
    status: str = ""
    reason: str = ""
    message: str = ""

    lastUpdateTime: datetime.datetime = ""
    lastTransitionTime: datetime.datetime = ""


class EndpointStatus(BaseModel):
    status: str = ""
    reason: str = ""
    message: str = ""

    replicas: int = 0
    availableReplicas: int = 0

    deploymentStatus: str = ""
    deploymentReason: str = ""
    deploymentMessage: str = ""
    deploymentLastUpdateTime: str = ""
    deploymentCondition: list[DeploymentCondition] = None

    lastUpdateTime: str = ""
    extraData: dict = None


class Getter:
    """
    Getter for kubernetes resource status
    """

    def __init__(self, kubeconfig_path, namespace):
        # 加载kubeconfig
        config.load_kube_config(config_file=kubeconfig_path)
        self.api_instance = client.AppsV1Api()
        self.namespace = namespace

    def deployment_status(self, deployment_name):
        """
        get deployment status
        """
        try:
            # 获取deployment信息
            resp = self.api_instance.read_namespaced_deployment(
                deployment_name, self.namespace
            )

            endpoint_status = EndpointStatus(
                deploymentStatus="Init",
                replicas=resp.status.replicas,
                availableReplicas=resp.status.available_replicas,
                extraData={
                    "observedGeneration": resp.status.observed_generation,
                    "updatedReplicas": resp.status.updated_replicas,
                    "readyReplicas": resp.status.ready_replicas,
                    "unavailableReplicas": resp.status.unavailable_replicas,
                    "collisionCount": resp.status.collision_count,
                },
            )
            if len(resp.status.conditions) == 0:
                return EndpointStatus()

            endpoint_status.deploymentCondition = []
            replica_failure_condition = None

            for condition in resp.status.conditions:
                endpoint_status.deploymentCondition.append(
                    DeploymentCondition(
                        type=condition.type,
                        status=condition.status,
                        lastUpdateTime=condition.last_update_time,
                        lastTransitionTime=condition.last_transition_time,
                        reason=condition.reason,
                        message=condition.message,
                    )
                )

                if condition.type == "Available":
                    endpoint_status.reason = condition.reason
                    endpoint_status.message = condition.message
                    endpoint_status.lastUpdateTime = condition.last_update_time

                    if (
                            condition.status == "True"
                            and condition.reason == "MinimumReplicasAvailable"
                    ):
                        endpoint_status.status = "Available"

                elif condition.type == "Progressing":
                    endpoint_status.deploymentReason = condition.reason
                    endpoint_status.deploymentMessage = condition.message
                    endpoint_status.deploymentLastUpdateTime = (
                        condition.last_transition_time
                    )

                    if condition.status == "True":
                        if condition.reason == "NewReplicaSetAvailable":
                            endpoint_status.deploymentStatus = "Completed"
                            continue
                        endpoint_status.deploymentStatus = "Progressing"
                    elif condition.Status == "False":
                        endpoint_status.deploymentStatus = "Failed"

                elif condition.type == "ReplicaFailure":
                    replica_failure_condition = condition

            if replica_failure_condition:
                endpoint_status.deploymentStatus = "Progressing"
                endpoint_status.deploymentReason = replica_failure_condition.reason
                endpoint_status.deploymentMessage = replica_failure_condition.message
                endpoint_status.deploymentLastUpdateTime = (
                    replica_failure_condition.last_update_time
                )

            return endpoint_status
        except client.ApiException as e:
            error_dict = json.loads(e.body)
            if e.status == 404:
                return EndpointStatus(
                    deploymentStatus="NotFound",
                    deploymentReason=e.reason,
                    deploymentMessage=error_dict["message"],
                )
            return EndpointStatus(
                deploymentStatus="Error",
                deploymentReason=e.reason,
                deploymentMessage=error_dict["message"],
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--deployment",
        dest="deployment",
        required=True,
        help="kubernetes deployment",
    )
    parser.add_argument(
        "-c",
        "--kube-config",
        dest="kube_config",
        required=True,
        help="kubernetes config path",
    )
    parser.add_argument(
        "-n",
        "--namespace",
        dest="namespace",
        required=False,
        default="default",
        help="kubernetes namespace",
    )

    args = parser.parse_args()

    status = Getter(args.kube_config, args.namespace).deployment_status(
        args.deployment
    )
    if status is not None:
        print(status.json())
