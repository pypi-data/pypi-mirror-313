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
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator


class Qunjielong(object):
    """
    Qunjielong Class

    @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
    """

    def __init__(
            self,
            base_url: str = "https://openapi.qunjielong.com/",
            secret: str = None,
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        """
        Qunjielong Class

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
        :param base_url:
        :param secret:
        :param cache:
        """
        base_url = base_url if isinstance(base_url, str) else "https://openapi.qunjielong.com/"
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.secret = secret if isinstance(secret, str) else ""
        self.cache = cache if isinstance(cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)) else None
        self.access_token = ""

    def _default_response_handler(self, response: requests.Response):
        if isinstance(response, requests.Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
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
            }).is_valid(json_addict):
                return json_addict.data, response
            return None, response

    def get_ghome_info(
            self,
            method: str = "GET",
            url: str = "/open/api/ghome/getGhomeInfo",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=09b80879-ddcb-49bf-b1e9-33181913924d
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "GET"
        url = url if isinstance(url, str) else "/open/api/ghome/getGhomeInfo"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        result, _ = self._default_response_handler(response)
        if not Draft202012Validator({
            "type": "object",
            "properties": {
                "ghId": {"type": "integer", "minimum": 1},
            },
            "required": ["ghId"]
        }).is_valid(result):
            return result, response
        return None, response

    def token_with_cache(
            self,
            expire: Union[float, int, timedelta] = None,
            token_kwargs: dict = None,
            get_ghome_info_kwargs: dict = None
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param token_kwargs: self.token kwargs
        :param get_ghome_info_kwargs: self.get_ghome_info kwargs
        :return:
        """
        token_kwargs = token_kwargs if isinstance(token_kwargs, dict) else {}
        get_ghome_info_kwargs = get_ghome_info_kwargs if isinstance(get_ghome_info_kwargs, dict) else {}
        cache_key = f"py3_qunjielong_access_token_{self.secret}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)
        ghome_info, r = self.get_ghome_info(**get_ghome_info_kwargs)
        if not isinstance(ghome_info, dict) or not int(ghome_info.get("ghId")):
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
            method: str = "GET",
            url: str = "/open/auth/token",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=71e7934a-afce-4fd3-a897-e2248502cc94
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "GET"
        url = url if isinstance(url, str) else "/open/auth/token"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("secret", self.secret)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        result, _ = self._default_response_handler(response)
        if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(result):
            self.access_token = result
        return self

    def list_act_info(
            self,
            act_no_list: Union[tuple, list] = None,
            method: str = "POST",
            url: str = "/open/api/act/list_act_info",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=e1171d6b-49f2-4ff5-8bd6-5b87c8290460
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/act/list_act_info"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        kwargs["json"] = {
            "actNoList": act_no_list,
        }
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def query_act_goods(
            self,
            act_no: Union[int, str] = None,
            method: str = "POST",
            url: str = "/open/api/act_goods/query_act_goods",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=55313bca-15ac-4c83-b7be-90e936829fe5
        :param act_no:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/act_goods/query_act_goods"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        kwargs["json"] = {
            "actNo": act_no,
        }
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def get_goods_detail(
            self,
            goods_id: Union[int, str] = None,
            method: str = "GET",
            url: str = f"/open/api/goods/get_goods_detail",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=55313bca-15ac-4c83-b7be-90e936829fe5
        :param goods_id:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "GET"
        url = f"{url}/{goods_id}" if isinstance(url, str) else f"/open/api/act_goods/query_act_goods/{goods_id}"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def query_order_list_with_forward(
            self,
            method: str = "POST",
            url: str = "/open/api/order/forward/query_order_list",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=06d169ae-68ac-11eb-a95d-1c34da7b354c
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/order/forward/query_order_list"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def query_order_list_with_reverse(
            self,
            method: str = "POST",
            url: str = "/open/api/order/reverse/query_order_list",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=06d5db35-68ac-11eb-a95d-1c34da7b354c
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/order/reverse/query_order_list"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def query_order_list_with_all(
            self,
            method: str = "POST",
            url: str = "/open/api/order/all/query_order_list",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=a43156d1-2fa8-4ea6-9fb3-b550ceb7fe44
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/order/all/query_order_list"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def query_order_info(
            self,
            order_no: Union[int, str] = None,
            method: str = "POST",
            url: str = "/open/api/order/single/query_order_info",
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=82385ad9-b3c5-4bcb-9e7a-2fbffd9fa69a
        :param order_no:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/open/api/order/single/query_order_info"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("accessToken", self.access_token)
        kwargs["params"] = params
        kwargs["json"] = {
            "orderNo": order_no,
        }
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)
