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

from typing import Any, Union
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class Webhook:
    """
    企业微信 Webhook Class
    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com",
            key: str = None,
            mentioned_list: Union[tuple, list] = None,
            mentioned_mobile_list: Union[tuple, list] = None
    ):
        """
        企业微信 Webhook Class
        :param base_url: base url
        :param key: key
        :param mentioned_list: mentioned list
        :param mentioned_mobile_list: mentioned mobile list
        """
        base_url = base_url if isinstance(base_url, str) else "https://qyapi.weixin.qq.com/"
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.key = key if isinstance(key, str) else ""
        self.mentioned_list = mentioned_list if isinstance(mentioned_list, (tuple, list)) else []
        self.mentioned_mobile_list = mentioned_mobile_list if isinstance(mentioned_mobile_list, (tuple, list)) else []

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
                return json_addict.get("media_id", True), response
        return False, response

    def send(
            self,
            method: str = "POST",
            url: str = "/cgi-bin/webhook/send",
            **kwargs
    ):
        """
        webhook send
        :param method: requests.request method
        :param url: requests.request url
        :param kwargs: requests.request kwargs
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/cgi-bin/webhook/send"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("key", self.key)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)

    def send_text(
            self,
            content: str = None,
            mentioned_list: Union[tuple, list] = None,
            mentioned_mobile_list: Union[tuple, list] = None,
            **kwargs
    ):
        """
        webhook send text

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :param kwargs:
        :return:
        """
        mentioned_list = mentioned_list if (isinstance(mentioned_list, (tuple, list))) else []
        mentioned_mobile_list = mentioned_mobile_list if (isinstance(mentioned_mobile_list, (tuple, list))) else []
        return self.send(
            json={
                "msgtype": "text",
                "text": {
                    "content": f"{content}",
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            },
            **kwargs
        )

    def send_markdown(
            self,
            content: str = None,
            **kwargs
    ):
        """
        webhook send markdown

        @see https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :param kwargs:
        :return:
        """
        return self.send(
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": f"{content}",
                }
            },
            **kwargs
        )

    def send_image(
            self,
            image_base64: str = None,
            **kwargs
    ):
        """
        webhook send image

        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B
        :param base64_string:
        :param kwargs:
        :return:
        """
        return self.send(
            json={
                "msgtype": "image",
                "image": {
                    "base64": f"{image_base64}",
                    "md5": "MD5",
                }
            },
            **kwargs
        )

    def send_news(
            self,
            articles: list = None,
            **kwargs
    ):
        """
        webhook send news

        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E6%96%87%E7%B1%BB%E5%9E%8B
        :param articles:
        :param kwargs:
        :return:
        """
        articles = articles if isinstance(articles, list) else []
        return self.send(
            json={
                "msgtype": "news",
                "news": {
                    "articles": articles,
                }
            },
            **kwargs
        )

    def send_file(
            self,
            media_id: str = None,
            **kwargs
    ):
        """
        webhook send file

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param kwargs:
        :return:
        """
        return self.send(
            json={
                "msgtype": "file",
                "file": {
                    "media_id": f"{media_id}"
                }
            },
            **kwargs
        )

    def send_voice(
            self,
            media_id: str = None,
            **kwargs
    ):
        """
        webhook send voice

        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :param kwargs:
        :return:
        """
        return self.send(
            json={
                "msgtype": "voice",
                "voice": {
                    "media_id": f"{media_id}"
                }
            },
            **kwargs
        )

    def send_template_card(
            self,
            template_card: Any = None,
            **kwargs
    ):
        """
        webhook send template card

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%A8%A1%E7%89%88%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B
        :param template_card:
        :param kwargs:
        :return:
        """
        template_card = template_card if isinstance(template_card, dict) else {}
        return self.send(
            json={
                "msgtype": "template_card",
                "template_card": template_card,
            },
            **kwargs
        )

    def upload_media(
            self,
            types: str = None,
            method: str = "POST",
            url: str = "/cgi-bin/webhook/upload_media",
            **kwargs
    ):
        """
        webhook upload media

        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param types:
        :param method:
        :param url:
        :param files:
        :param kwargs:
        :return:
        """
        types = types if types in ["file", "voice"] else "file"
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/cgi-bin/webhook/send"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        params = kwargs.get("params", {})
        params.setdefault("key", self.key)
        params.setdefault("type", types)
        kwargs["params"] = params
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        return self._default_response_handler(response)
