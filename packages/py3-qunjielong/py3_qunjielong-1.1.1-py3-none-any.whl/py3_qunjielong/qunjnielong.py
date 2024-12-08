#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_qunjielong
=================================================
"""
from datetime import timedelta
from typing import Union

import diskcache
import py3_requests
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl:
    """
    url settings
    """
    BASE_URL = "https://openapi.qunjielong.com/"
    GET_GHOME_INFO_URL = "/open/api/ghome/getGhomeInfo"
    TOKEN_URL = "/open/auth/token"
    LIST_ACT_INFO_URL = "/open/api/act/list_act_info"
    QUERY_ACT_GOODS_URL = "/open/api/act_goods/query_act_goods"
    GET_GOODS_DETAIL_URL = "/open/api/goods/get_goods_detail"
    FORWARD_QUERY_ORDER_LIST_URL = "/open/api/order/forward/query_order_list"
    REVERSE_QUERY_ORDER_LIST_URL = "/open/api/order/reverse/query_order_list"
    ALL_QUERY_ORDER_LIST_URL = "/open/api/order/all/query_order_list"
    QUERY_ORDER_INFO_URL = "/open/api/order/single/query_order_info"


class ValidatorJsonSchema:
    """
    json schema settings
    """
    NORMAL_SCHEMA = {
        "type": "object",
        "properties": {
            "code": {
                "oneOf": [
                    {"type": "integer", "const": 200},
                    {"type": "string", "const": 200},
                ],
            }
        },
        "required": ["code"],
    }

    GET_GHOME_INFO_SCHEMA = {
        "type": "object",
        "properties": {
            "ghId": {"type": "integer", "minimum": 1},
        },
        "required": ["ghId"]
    }


class ResponseHandler:
    """
    response handler
    """

    @staticmethod
    def normal_handler(response: Response = None):
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator(ValidatorJsonSchema.NORMAL_SCHEMA).is_valid(instance=json_addict):
                return json_addict.get("data", None)
            return None
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Qunjielong(object):
    """
    Qunjielong Class

    @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
    """

    def __init__(
            self,
            base_url: str = RequestUrl.BASE_URL,
            secret: str = "",
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        """
        Qunjielong Class

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
        :param base_url:
        :param secret:
        :param cache:
        """
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.secret = secret
        self.cache = cache
        self.access_token = ""

    def request_with_token(self, **kwargs):
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "get")
        kwargs.setdefault("url", "")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("accessToken", self.access_token)
        return py3_requests.request(**kwargs.to_dict())

    def get_ghome_info(
            self,
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=09b80879-ddcb-49bf-b1e9-33181913924d
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", RequestUrl.GET_GHOME_INFO_URL)
        return self.request_with_token(**kwargs.to_dict())

    def token_with_cache(
            self,
            expire: Union[float, int, timedelta] = None,
            token_kwargs: dict = {},
            get_ghome_info_kwargs: dict = {}
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param token_kwargs: self.token kwargs
        :param get_ghome_info_kwargs: self.get_ghome_info kwargs
        :return:
        """
        cache_key = f"py3_qunjielong_access_token_{self.secret}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)

        if not Draft202012Validator(ValidatorJsonSchema.GET_GHOME_INFO_SCHEMA).is_valid(
                self.get_ghome_info(**get_ghome_info_kwargs)
        ):
            self.token(**token_kwargs)
            if isinstance(self.access_token, str) and len(self.access_token):
                if isinstance(self.cache, diskcache.Cache):
                    self.cache.set(
                        key=cache_key,
                        value=self.access_token,
                        expire=expire or timedelta(seconds=7100).total_seconds()
                    )
                if isinstance(self.cache, (redis.Redis, redis.StrictRedis)):
                    self.cache.setex(
                        name=cache_key,
                        value=self.access_token,
                        time=expire or timedelta(seconds=7100),
                    )

        return self

    def token(
            self,
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=71e7934a-afce-4fd3-a897-e2248502cc94
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", RequestUrl.TOKEN_URL)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("secret", self.secret)
        result = py3_requests.request(**kwargs.to_dict())
        if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(result):
            self.access_token = result
        return self
