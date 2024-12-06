# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time    : 2024/12/2 下午2:46
# @Author  : haosixu
# @File    : subscription_client.py
# @Software: PyCharm
"""

from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from .subscription_api import CheckEquityRequest


class SubscriptionClient(BceInternalClient):
    """
    A client class for interacting with the compute service. Initializes with default configuration.
    This client provides an interface to interact with the subscription service using BCE (Baidu Cloud Engine) API.
    """

    def check_equity(self,
                     req: CheckEquityRequest):
        """
        Check equity info.
        Args:
            equty_id (str): 权益标识

        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/subscribe-equity/check-info", encoding="utf-8"),
                                  params=req.json(by_alias=True))