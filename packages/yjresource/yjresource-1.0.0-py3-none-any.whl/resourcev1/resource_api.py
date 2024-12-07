# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time    : 2024/12/6 上午11:45
# @Author  : haosixu
# @File    : resource_api.py
# @Software: PyCharm
"""
from typing import Optional
from pydantic import BaseModel, Field

class Record(BaseModel):
    """
    Record model.
    """
    uuid: str = Field(..., description="UUID 唯一标识")
    org_id: str = Field(..., alias="orgID", description="租户id")
    compute: Optional[str] = Field(None, description="计算资源, windmill compute name")
    accelerator_type: Optional[str] = Field(None, alias="acceleratorType", description="卡的类型")
    accelerator_count: Optional[int] = Field(None, alias="acceleratorCount", description="卡的数量")
    object_type: str = Field(..., alias="objectType", description="对象类型, example: 'job','endpoint','multimodal','datasource'")
    object_id: Optional[str] = Field(None, alias="objectID", description="对象标识")
    metric: str = Field(..., description="统计项")
    value: str = Field(..., description="统计项的取值")
    timestamp: int = Field(..., description="时间戳（单位秒）")

class CreateRecordRequest(BaseModel):
    """
    Create record request.
    """
    records: list[Record] = Field(..., description="记录列表")