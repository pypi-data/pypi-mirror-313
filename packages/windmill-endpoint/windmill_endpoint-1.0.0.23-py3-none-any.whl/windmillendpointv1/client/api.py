# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/8/13 14:13
# @Author : zhangzhijun06
# @Email: zhangzhijun06@baidu.com
# @File : __init__.py.py
# @Software: PyCharm
"""
from pydantic import BaseModel
from typing import Union, Any, List


class ModelMetaData(BaseModel):
    """model meta data"""
    image_id: str = ""
    camera_id: str = ""
    camera_fps: int = 25
    frame_pos: int = 0
    timestamp: str = ""

    block_scale_width: float = 1.0
    block_scale_height: float = 1.0
    block_offset_width: float = 0
    block_offset_height: float = 0
    whole_scale_width: float = 1.0
    whole_scale_height: float = 1.0


class ModelInferRequest(BaseModel):
    """model inference request"""
    meta: ModelMetaData = None
    image_buffer: bytes = b""
    model_name: str = "ensemble"


class OCR(BaseModel):
    """OCR"""
    word: str = ""
    direction: Union[str, int] = ""
    confidence: float = 0.0


class Category(BaseModel):
    """Category"""
    id: str = ""
    name: str = ""
    confidence: float = 0.0
    value: Any = None


class Prediction(BaseModel):
    """Prediction"""
    bbox: List[float] = None
    confidence: float = 0.0
    segmentation: List[float] = None
    area: float = 0.0
    ocr: OCR = None
    features: List[float] = None
    bbox_id: int = 0
    track_id: int = 0
    categories: List[Category] = None


class Parameter(BaseModel):
    """Parameter"""
    name: str = ""
    namespace: str = ""
    type: str = ""
    current: str = ""
    default: str = ""
    description: str = ""
    step: str = ""
    range: str = ""
    enum: str = ""
    exclude: str = ""


class ModelParameter(BaseModel):
    """ModelParameter"""
    model_name: str = ""
    model_type: str = ""
    parameters: List[Parameter] = None


class ModelInferOutput(BaseModel):
    """ModelInferOutput"""
    image_id: str = ""
    predictions: List[Prediction] = None
    model_parameters: List[ModelParameter] = None
