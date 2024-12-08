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

import py3_requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class ReqeustUrl:
    BASE_URL: str = "https://speaker.17laimai.cn/"
    NOTIFY_URL: str = "/notify.php"


class ValidatorJsonSchema:
    NORMAL_SCHEMA = {
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
    }


class ResponseHandler:
    @staticmethod
    def normal_handler(response: Response = None):
        if isinstance(response, Response):
            json_addict = Dict(response.json())
            if Draft202012Validator(ValidatorJsonSchema).is_valid(json_addict):
                return True
            return False
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Speaker(object):
    """
    brhk speaker class

    @see https://www.yuque.com/lingdutuandui
    """

    def __init__(
            self,
            base_url: str = ReqeustUrl.BASE_URL,
            token: str = "",
            id: str = "",
            version: Union[int, str] = "1"
    ):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.token = token
        self.id = id
        self.version = version

    def notify(
            self,
            message: str = None,
            **kwargs
    ):
        """
        notify

        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#teXR7
        :param message:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("url", f"{ReqeustUrl.NOTIFY_URL}")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("data", Dict())
        kwargs.data.setdefault("token", self.token)
        kwargs.data.setdefault("id", self.id)
        kwargs.data.setdefault("version", self.version)
        kwargs.data.setdefault("message", message)
        return py3_requests.request(
            **kwargs.to_dict()
        )
