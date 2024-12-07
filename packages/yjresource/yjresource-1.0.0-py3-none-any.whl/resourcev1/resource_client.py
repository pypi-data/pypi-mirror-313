# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time    : 2024/12/6 11:46
# @Author  : haosixu
# @File    : resource_client.py
# @Software: PyCharm
"""

from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from .resource_api import CreateRecordRequest


class ResourceClient(BceInternalClient):
    """
    This client provides an interface to interact with the resource service using BCE (Baidu Cloud Engine) API.
    """

    def create_record(self,
                     req: CreateRecordRequest):
        """
        Create record
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/resources/records", encoding="utf-8"),
                                  params=req.json(by_alias=True))