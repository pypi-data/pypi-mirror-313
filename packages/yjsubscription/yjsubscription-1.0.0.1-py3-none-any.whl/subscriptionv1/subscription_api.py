# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time    : 2024/12/3 上午11:45
# @Author  : haosixu
# @File    : subscription_api.py
# @Software: PyCharm
"""
from pydantic import BaseModel, Field

class CheckEquityRequest(BaseModel):
    """
    Check equity request.
    """
    equty_id: str = Field(alias="equtyID")

class CheckEquityResponse(BaseModel):
    """
    Check equity response.
    """
    check_result: str = Field(alias="checkResult")
    validity_end_date: int = Field(alias="validityEndDate")
    total: int = Field(alias="total")
    used: int = Field(alias="used")

