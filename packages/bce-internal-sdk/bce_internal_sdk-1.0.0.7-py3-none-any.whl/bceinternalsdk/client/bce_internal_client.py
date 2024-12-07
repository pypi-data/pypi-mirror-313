#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/1/25 14:13
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : bce_internal_client.py
# @Software: PyCharm
"""
from typing import Optional
from baidubce.http import bce_http_client
from baidubce import compat
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.http import handler
from baidubce.bce_client_configuration import BceClientConfiguration
import json


class BceInternalClient(BceBaseClient):
    """
    A client class for interacting with bce service. Initializes with default configuration.

    This client provides an interface to interact with the Artifact service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving artifacts within a specified workspace.

    Args:
        config (Optional[BceClientConfiguration]): The client configuration to use.
        ak (Optional[str]): Access key for authentication.
        sk (Optional[str]): Secret key for authentication.
        endpoint (Optional[str]): The service endpoint URL.
        context (Optional[dict]): The user context.
    """

    def __init__(
        self,
        config: Optional[BceClientConfiguration] = None,
        ak: Optional[str] = "",
        sk: Optional[str] = "",
        endpoint: Optional[str] = "",
        context: Optional[dict] = None,
    ):
        if config is None:
            config = BceClientConfiguration(credentials=BceCredentials(ak, sk),
                                            endpoint=endpoint)
        self.context = context
        super(BceInternalClient, self).__init__(config=config)

    def _send_request(self,
                      http_method,
                      path,
                      headers=None,
                      params=None,
                      body=None):
        """
        Send request to the bce service.
        """
        if self.context is not None:
            headers = dict()
            headers[b"x-impersonate-target-org-id"] = self.context.get(
                "OrgID", "").encode("utf-8")
            headers[b"x-impersonate-target-user-id"] = self.context.get(
                "UserID", "").encode("utf-8")
            headers[b"x-impersonate-target-project-id"] = self.context.get(
                "ProjectID", "").encode("utf-8")
        return bce_http_client.send_request(
            self.config,
            sign([b"host", b"x-bce-date"]),
            [handler.parse_error, parse_json],
            http_method,
            path,
            body,
            headers,
            params,
        )


def sign(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""

    def _wrapper(credentials, http_method, path, headers, params):
        credentials.access_key_id = compat.convert_to_bytes(
            credentials.access_key_id)
        credentials.secret_access_key = compat.convert_to_bytes(
            credentials.secret_access_key)

        return bce_v1_signer.sign(
            credentials,
            compat.convert_to_bytes(http_method),
            compat.convert_to_bytes(path),
            headers,
            params,
            headers_to_sign=headers_to_sign,
        )

    return _wrapper


def parse_json(http_response, response):
    """If the body is not empty, convert it to a python object and set as the value of
    response.body. http_response is always closed if no error occurs.

    :param http_response: the http_response object returned by HTTPConnection.getresponse()
    :type http_response: httplib.HTTPResponse

    :param response: general response object which will be returned to the caller
    :type response: baidubce.BceResponse

    :return: always true
    :rtype bool
    """
    body = http_response.read()
    if body:
        body = compat.convert_to_string(body)
        response.__dict__.update(json.loads(body))
        response.__dict__["raw_data"] = body
    http_response.close()
    return True
