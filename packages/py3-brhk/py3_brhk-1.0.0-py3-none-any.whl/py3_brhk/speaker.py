#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_brhk
=================================================
"""
from typing import Union

import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class Speaker(object):
    """
    brhk speaker class

    @see https://www.yuque.com/lingdutuandui
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn",
            token: str = "",
            id: str = "",
            version: Union[int, str] = "1"
    ):
        base_url = base_url if isinstance(base_url, str) else "https://speaker.17laimai.cn"
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.token = token if isinstance(token, str) else token
        self.id = id if isinstance(id, str) else id
        self.version = version if isinstance(version, (int, str)) else version

    def _default_response_handler(self, response: Response = None):
        """
        default response handler
        :param response: requests.Response instance
        :return:
        """
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "errcode": {
                        "oneOf": [
                            {"type": "integer", "const": 0},
                            {"type": "string", "const": "0"},
                        ]
                    }
                },
                "required": ["errcode"]
            }).is_valid(json_addict):
                return True, response
        return False, response

    def notify(
            self,
            message: str = None,
            method: str = "POST",
            url: str = "/notify.php",
            **kwargs
    ):
        """
        notify

        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#teXR7
        :param message:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/notify.php"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        data = kwargs.get("data", {})
        data.setdefault("token", self.token)
        data.setdefault("id", self.id)
        data.setdefault("version", self.version)
        data.setdefault("message", message)
        kwargs["data"] = data
        response = requests.request(method=method, url=url, **kwargs)
        return self._default_response_handler(response)
