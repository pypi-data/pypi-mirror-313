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
from typing import Union, Callable

import diskcache
import py3_requests
import redis
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl:
    BASE_URL = "https://qyapi.weixin.qq.com/"
    GETTOKEN_URL = "/cgi-bin/gettoken"
    GET_API_DOMAIN_IP_URL = "/cgi-bin/get_api_domain_ip"
    MESSAGE_SEND_URL = "/cgi-bin/message/send"
    MEDIA_UPLOAD_URL = "/cgi-bin/media/upload"
    MEDIA_UPLOADIMG_URL = "/cgi-bin/media/uploadimg"


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
        "required": ["errcode"],
    }

    GETTOKEN_SCHEMA = {
        "type": "object",
        "properties": {
            "access_token": {"type": "string", "minLength": 1},
        },
        "required": ["access_token"],
    }

    GET_API_DOMAIN_IP_SCHEMA = {
        "type": "object",
        "properties": {
            "ip_list": {"type": "array", "minItem": 1},
        },
        "required": ["ip_list"],
    }

    MEDIA_UPLOAD_SCHEMA = {
        "type": "object",
        "properties": {
            "media_id": {"type": "string", "minLength": 1},
        },
        "required": ["ip_list"],
    }

    MEDIA_UPLOADIMG_SCHEMA = {
        "type": "object",
        "properties": {
            "media_id": {"type": "string", "minLength": 1},
        },
        "required": ["ip_list"],
    }


class ResponseHandler:
    @staticmethod
    def default_handler(response: Response = None):
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator(ValidatorJsonSchema.NORMAL_SCHEMA).is_valid(instance=json_addict):
                return json_addict
            return None
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Server:
    """
    Server API Class

    @see https://developer.work.weixin.qq.com/document/path/90664
    """

    def __init__(
            self,
            base_url: str = RequestUrl.BASE_URL,
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None
    ):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.cache = cache
        self.access_token = ""

    def request_with_token(self, response_handler: Callable = ResponseHandler.default_handler, **kwargs):
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", f"{self.base_url}{kwargs.get('url', '')}")
        kwargs.params.setdefault("access_token", self.access_token)
        return py3_requests.request(**kwargs.to_dict())

    def get_api_domain_ip(
            self,
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
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", RequestUrl.GET_API_DOMAIN_IP_URL)
        result = self.request_with_token(**kwargs.to_dict());
        if Draft202012Validator(ValidatorJsonSchema.GET_API_DOMAIN_IP_SCHEMA).is_valid(result):
            return result.get("ip_list", None)
        return None

    def gettoken_with_cache(
            self,
            expire: Union[float, int, timedelta] = 7100,
            gettoken_kwargs: dict = {},
            get_api_domain_ip_kwargs: dict = {}
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param gettoken_kwargs: self.gettoken kwargs
        :param get_api_domain_ip_kwargs: self.get_api_domain_ip kwargs
        :return:
        """
        cache_key = f"py3_workwx_access_token_{self.agentid}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)
        if Draft202012Validator(ValidatorJsonSchema.GET_API_DOMAIN_IP_SCHEMA).is_valid(
                self.get_api_domain_ip(**get_api_domain_ip_kwargs)
        ):
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
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.default_handler)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", f"{self.base_url}{RequestUrl.GETTOKEN_URL}")
        kwargs.params.setdefault("corpid", self.corpid)
        kwargs.params.setdefault("corpsecret", self.corpsecret)
        result = py3_requests.request(
            **kwargs.to_dict(),
        )
        if Draft202012Validator(ValidatorJsonSchema.GETTOKEN_SCHEMA).is_valid(result):
            self.access_token = result.get("access_token", None)
        return self

    def message_send(
            self,
            **kwargs
    ):
        """
        message send

        @see https://developer.work.weixin.qq.com/document/path/90236
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.default_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MESSAGE_SEND_URL)
        return self.request_with_token(**kwargs.to_dict())

    def media_upload(
            self,
            **kwargs
    ):
        """
        media upload

        @see https://developer.work.weixin.qq.com/document/path/90253
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.default_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MEDIA_UPLOAD_URL)
        result = self.request_with_token(**kwargs.to_dict())
        if Draft202012Validator(ValidatorJsonSchema.MEDIA_UPLOAD_SCHEMA).is_valid(result):
            return result.get("media_id", None)
        return None

    def uploadimg(
            self,
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
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.default_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MEDIA_UPLOADIMG_URL)
        result = self.request_with_token(**kwargs.to_dict())
        if Draft202012Validator(ValidatorJsonSchema.MEDIA_UPLOADIMG_SCHEMA).is_valid(result):
            return result.get("url", None)
        return None
