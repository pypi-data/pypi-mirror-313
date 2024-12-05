# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/8/13 14:13
# @Author : zhangzhijun06
# @Email: zhangzhijun06@baidu.com
# @File : __init__.py.py
# @Software: PyCharm
"""
import os
import random
import numpy as np
import json
from typing import Union, List
from PIL import Image, ImageDraw
import tritonclient.http as http_client
import tritonclient.grpc as grpc_client
from tritonv2.http_client import TritonHTTPClient
from tritonv2.grpc_client import TritonGRPCClient
from tritonclient.utils import triton_to_np_dtype
from tritonv2.utils import list_stack_ndarray
from .api import ModelInferRequest, ModelInferOutput


def infer(triton_client: Union[TritonHTTPClient, TritonGRPCClient],
          req: ModelInferRequest) -> List[ModelInferOutput]:
    """
    model inference using triton http client
    Args:
        triton_client: triton client(http/grpc).
        req: model infer request.
    """
    input_metadata, output_metadata, batch_size = (
            triton_client.get_inputs_and_outputs_detail(model_name=req.model_name))
    # 处理数据
    # 1. 读取图片
    repeated_image_data = []
    img = np.frombuffer(req.image_buffer, dtype=triton_to_np_dtype(input_metadata[0]['datatype']))
    repeated_image_data.append(np.array(img))
    batched_image_data = list_stack_ndarray(repeated_image_data)
    # 2. 添加meta信息
    meta_json = json.dumps(req.meta.__dict__)
    byte_meta_json = meta_json.encode()
    np_meta_json = np.frombuffer(byte_meta_json, dtype='uint8')
    send_meta_json = np.array(np_meta_json)
    send_meta_json = np.expand_dims(send_meta_json, axis=0)

    # build triton input
    if isinstance(triton_client, TritonHTTPClient):
        inputs = [
            http_client.InferInput(input_metadata[0]["name"], list(
                batched_image_data.shape), input_metadata[0]["datatype"]),
            http_client.InferInput(input_metadata[1]["name"], send_meta_json.shape,
                                   input_metadata[1]["datatype"])
        ]
        inputs[0].set_data_from_numpy(batched_image_data, binary_data=False)
        inputs[1].set_data_from_numpy(send_meta_json)
    else:
        inputs = [
            grpc_client.InferInput(input_metadata[0]["name"], list(
                batched_image_data.shape), input_metadata[0]["datatype"]),
            grpc_client.InferInput(input_metadata[1]["name"], send_meta_json.shape,
                                   input_metadata[1]["datatype"])
        ]
        inputs[0].set_data_from_numpy(batched_image_data)
        inputs[1].set_data_from_numpy(send_meta_json)

    # build triton output
    output_names = [
        output["name"] for output in output_metadata
    ]
    outputs = []
    if isinstance(triton_client, TritonHTTPClient):
        for output_name in output_names:
            outputs.append(
                http_client.InferRequestedOutput(output_name, binary_data=True))
    else:
        for output_name in output_names:
            outputs.append(
                grpc_client.InferRequestedOutput(output_name))

    # infer result
    result = triton_client.model_infer(req.model_name, inputs, outputs=outputs)
    for output_name in output_names:
        response = eval(result.as_numpy(output_name))

    resp_list = []
    for item in response:
        resp_list.append(ModelInferOutput(**item))
    return resp_list


def draw_bbox(img_path, infer_result, output_path):
    """
    draw bbox on image
    """
    boxes, labels = [], []
    image = Image.open(img_path).convert("RGB")

    predictions = infer_result[0].predictions
    for pred in predictions:
        bbox = pred.bbox
        class_name = pred.categories[0].name
        boxes.append([int(bbox[0]), int(bbox[1]), int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])])
        labels.append(class_name)

    draw = ImageDraw.Draw(image)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for bbox, label in zip(boxes, labels):
        draw.rectangle(bbox, outline=color, width=2)

    # Save the result
    file_name = os.path.basename(img_path)
    image.save(os.path.join(output_path, file_name))
