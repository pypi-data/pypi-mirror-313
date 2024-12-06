#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_workwx
=================================================
"""
from datetime import timedelta
from typing import Union, Any

import diskcache
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class Server:
    """
    企业微信服务端 API Class
    @see https://developer.work.weixin.qq.com/document/path/91039
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            corpid: str = None,
            corpsecret: str = None,
            agentid: Union[int, str] = None,
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        base_url = base_url if isinstance(base_url, str) else "https://qyapi.weixin.qq.com/"
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.corpid = corpid if isinstance(corpid, str) else ""
        self.corpsecret = corpsecret if isinstance(corpsecret, str) else ""
        self.agentid = agentid if isinstance(agentid, (int, str)) else ""
        self.cache = cache if isinstance(cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)) else None
        self.access_token = ""

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
                "required": ["errcode"],
            }).is_valid(json_addict):
                return json_addict, response
        return False, response

    def get_api_domain_ip(
            self,
            method: str = "GET",
            url: str = "/cgi-bin/get_api_domain_ip",
            **kwargs
    ):
        """
        get api domain ip

        @see https://developer.work.weixin.qq.com/document/path/92520
        :param method: requests.request method
        :param url: requests.request url
        :param kwargs: requests.request kwargs
        :return:
        """
        method = method if isinstance(method, str) else "GET"
        url = url if isinstance(url, str) else "/cgi-bin/get_api_domain_ip"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("access_token", self.access_token)
        kwargs["params"] = params
        response = requests.request(method, url, **kwargs)
        return self._default_response_handler(response)

    def gettoken_with_cache(
            self,
            expire: Union[float, int, timedelta] = None,
            gettoken_kwargs: dict = None,
            get_api_domain_ip_kwargs: dict = None
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param gettoken_kwargs: self.gettoken kwargs
        :param get_api_domain_ip_kwargs: self.get_api_domain_ip kwargs
        :return:
        """
        gettoken_kwargs = gettoken_kwargs or {}
        get_api_domain_ip_kwargs = get_api_domain_ip_kwargs or {}
        cache_key = f"py3_workwx_access_token_{self.agentid}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)
        api_domain_ip, r = self.get_api_domain_ip(**get_api_domain_ip_kwargs)
        if not isinstance(api_domain_ip, dict) or not len(api_domain_ip.get("ip_list")):
            self.gettoken(**gettoken_kwargs)
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

    def gettoken(
            self,
            method: str = "GET",
            url: str = "/cgi-bin/gettoken",
            **kwargs
    ):
        """
        get access token

        @see https://developer.work.weixin.qq.com/document/path/91039
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "GET"
        url = url if isinstance(url, str) else "/cgi-bin/gettoken"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("corpid", self.corpid)
        params.setdefault("corpsecret", self.corpsecret)
        kwargs["params"] = params
        response = requests.request(method, url, **kwargs)
        result, _ = self._default_response_handler(response)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "access_token": {"type": "string", "minLength": 1},
            },
            "required": ["access_token"]
        }).is_valid(result):
            self.access_token = result.get("access_token", None)
        return self

    def message_send(
            self,
            method: str = "POST",
            url: str = "/cgi-bin/message/send",
            **kwargs
    ):
        """
        message send

        @see https://developer.work.weixin.qq.com/document/path/90236
        :param method:
        :param url:
        :param json_data:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/cgi-bin/message/send"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("access_token", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def media_upload(
            self,
            types: str = None,
            method: str = "POST",
            url: str = "/cgi-bin/media/upload",
            **kwargs
    ):
        """
        media upload

        @see https://developer.work.weixin.qq.com/document/path/90253
        :param types:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        types = types if types in ["file", "image", "voice", "video"] else "file"
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/cgi-bin/media/upload"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"

        params = kwargs.get("params", {})
        params.setdefault("access_token", self.access_token)
        params.setdefault("type", types)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        result, _ = self._default_response_handler(response)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "media_id": {"type": "string", "minLength": 1},
            },
            "required": ["media_id"]
        }).is_valid(result):
            return result.get("media_id", None), response
        return result, response

    def uploadimg(
            self,
            method: str = "POST",
            url: str = "/cgi-bin/media/uploadimg",
            **kwargs
    ):
        """
        upload image

        @see https://developer.work.weixin.qq.com/document/path/90256
        :param method:
        :param url:
        :param files:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/cgi-bin/media/uploadimg"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("access_token", self.access_token)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        result, _ = self._default_response_handler(response)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "url": {"type": "string", "minLength": 1},
            },
            "required": ["url"]
        }).is_valid(result):
            return result.get("url", None), response
        return result, response
