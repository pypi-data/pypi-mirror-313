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

from typing import Any, Union, Callable
from addict import Dict
import py3_requests
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl:
    """
    url settings
    """
    BASE_URL = "https://qyapi.weixin.qq.com/"
    SEND_URL = "/cgi-bin/webhook/send"
    UPLOAD_MEDIA_URL = "/cgi-bin/webhook/upload_media"


class ValidatorJsonSchema:
    """
    json schema settings
    """
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


class ResponseHandler:
    """
    response handler
    """

    @staticmethod
    def normal_handler(response: Response = None):
        if isinstance(response, Response) and response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator(ValidatorJsonSchema.NORMAL_SCHEMA).is_valid(instance=json_addict):
                return json_addict.get("media_id", True)
            return None
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Webhook:
    """
    Webhook Class

    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(
            self,
            base_url: str = RequestUrl.BASE_URL,
            key: str = "",
            mentioned_list: Union[tuple, list] = [],
            mentioned_mobile_list: Union[tuple, list] = []
    ):
        """
        Webhook Class

        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: base url, automatically remove the end /
        :param key: webhook url params.key value
        :param mentioned_list: mentioned userid list if message type == text enabled
        :param mentioned_mobile_list: mentioned mobile list if message type == text enabled
        """
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.key = key
        self.mentioned_list = mentioned_list
        self.mentioned_mobile_list = mentioned_mobile_list

    def send(
            self,
            response_handler: Callable = ResponseHandler.normal_handler,
            method: str = "POST",
            url: str = RequestUrl.SEND_URL,
            **kwargs
    ):
        """
        webhook send
        :param response_handler: py3_requests.request.response_handler
        :param method: py3_requests.request method
        :param url: py3_requests.request url
        :param kwargs: py3_requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("url", f"{self.base_url}{url}")
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("key", self.key)
        return py3_requests.request(
            **kwargs.to_dict()
        )

    def send_text(
            self,
            content: str = "",
            mentioned_list: Union[tuple, list] = [],
            mentioned_mobile_list: Union[tuple, list] = [],
            **kwargs
    ):
        """
        webhook send text

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param kwargs: webhook send kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "text")
        kwargs.json.text.setdefault("content", content)
        kwargs.json.text.setdefault("mentioned_list", self.mentioned_list + mentioned_list)
        kwargs.json.text.setdefault("mentioned_mobile_list", self.mentioned_mobile_list + mentioned_mobile_list)
        return self.send(**kwargs.to_dict())

    def send_markdown(
            self,
            content: str = "",
            **kwargs
    ):
        """
        webhook send markdown

        @see https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "markdown")
        kwargs.json.markdown.setdefault("content", content)
        return self.send(**kwargs.to_dict())

    def send_image(
            self,
            image_base64: str = "",
            **kwargs
    ):
        """
        webhook send image

        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B
        :param image_base64:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "image")
        kwargs.json.image.setdefault("base64", image_base64)
        kwargs.json.image.setdefault("md5", "MD5")
        return self.send(**kwargs.to_dict())

    def send_news(
            self,
            articles: list = [],
            **kwargs
    ):
        """
        webhook send news

        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E6%96%87%E7%B1%BB%E5%9E%8B
        :param articles:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "news")
        kwargs.json.news.setdefault("articles", articles)
        return self.send(**kwargs.to_dict())

    def send_file(
            self,
            media_id: str = "",
            **kwargs
    ):
        """
        webhook send file

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "file")
        kwargs.json.file.setdefault("media_id", media_id)
        return self.send(**kwargs.to_dict())

    def send_voice(
            self,
            media_id: str = "",
            **kwargs
    ):
        """
        webhook send voice

        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "voice")
        kwargs.json.voice.setdefault("media_id", media_id)
        return self.send(**kwargs.to_dict())

    def send_template_card(
            self,
            template_card: Union[dict, Dict] = {},
            **kwargs
    ):
        """
        webhook send template card

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%A8%A1%E7%89%88%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B
        :param template_card:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("json", Dict({}))
        kwargs.json.setdefault("msgtype", "template_card")
        kwargs.json.template_card.setdefault("template_card", template_card)
        return self.send(**kwargs.to_dict())

    def upload_media(
            self,
            response_handler: Callable = ResponseHandler.normal_handler,
            types: str = "file",
            files: Any = None,
            **kwargs
    ):
        """
        webhook upload media

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param response_handler: py3_requests.request response handler
        :param types: must be "file" or "voice"
        :param files: py3_requests.request files
        :param kwargs: py3_requests.request kwargs
        :return:
        """
        types = types.lower() if types.lower() in ["file", "voice"] else "file"
        kwargs = Dict(kwargs)
        kwargs.setdefault("params", Dict({}))
        kwargs.params.setdefault("key", self.key)
        kwargs.params.setdefault("type", types)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", f"{self.base_url}{RequestUrl.UPLOAD_MEDIA_URL}")
        return py3_requests.request(
            response_handler=response_handler,
            files=files,
            **kwargs.to_dict(),
        )
