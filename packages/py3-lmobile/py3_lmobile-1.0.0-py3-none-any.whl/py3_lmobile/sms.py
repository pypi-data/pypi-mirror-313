#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_lmobile
=================================================
"""
import hashlib
import string
from datetime import datetime
import random
from typing import Union

import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class SMS(object):
    """
    @see https://www.lmobile.cn/ApiPages/index.html
    """

    def __init__(
            self,
            base_url: str = "https://api.51welink.com/",
            account_id: str = "",
            password: str = "",
            product_id: Union[int, str] = 0,
            smms_encrypt_key: str = "SMmsEncryptKey",
    ):
        """
        @see https://www.lmobile.cn/ApiPages/index.html
        :param base_url:
        :param account_id:
        :param password:
        :param product_id:
        :param smms_encrypt_key:
        """
        base_url = base_url if isinstance(base_url, str) else "https://qyapi.weixin.qq.com/"
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.account_id = account_id if isinstance(account_id, str) else ""
        self.password = password if isinstance(password, str) else ""
        self.product_id = product_id if isinstance(product_id, (int, str)) else 0
        self.smms_encrypt_key = smms_encrypt_key if isinstance(smms_encrypt_key, str) else ""

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
                    "Result": {"type": "string", "const": "succ"},
                },
                "required": ["Result"]
            }).is_valid(json_addict):
                return True, response
        return False, response

    def timestamp(self):
        return int(datetime.now().timestamp())

    def random_digits(self, length=10):
        return int("".join(random.sample(string.digits, length)))

    def password_md5(self):
        return hashlib.md5(f"{self.password}{self.smms_encrypt_key}".encode('utf-8')).hexdigest()

    def sha256_signature(self, data: dict = {}):
        data = data if isinstance(data, dict) else dict()
        data.setdefault("AccountId", self.account_id)
        data.setdefault("Timestamp", self.timestamp())
        data.setdefault("Random", self.random_digits())
        data.setdefault("ProductId", self.product_id)
        data.setdefault("PhoneNos", "")
        data.setdefault("Content", "")
        temp_string = "&".join([
            f"AccountId={data.get("AccountId", "")}",
            f"PhoneNos={str(data.get("PhoneNos", "")).split(",")[0]}",
            f"Password={self.password_md5().upper()}",
            f"Random={data.get('Random', "")}",
            f"Timestamp={data.get('Timestamp', "")}",
        ])
        return hashlib.sha256(temp_string.encode("utf-8")).hexdigest()

    def send_sms(
            self,
            phone_nos: str = None,
            content: str = None,
            method: str = "POST",
            url: str = "/EncryptionSubmit/SendSms.ashx",
            **kwargs
    ):
        """
        @see https://www.lmobile.cn/ApiPages/index.html
        :param phone_nos:
        :param content:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/EncryptionSubmit/SendSms.ashx"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        data = kwargs.get("data", {})
        data.setdefault("AccountId", self.account_id)
        data.setdefault("Timestamp", self.timestamp())
        data.setdefault("Random", self.random_digits())
        data.setdefault("ProductId", self.product_id)
        data.setdefault("PhoneNos", phone_nos)
        data.setdefault("Content", content)
        data.setdefault("AccessKey", self.sha256_signature(data))
        kwargs["data"] = data
        response = requests.request(method=method, url=url, **kwargs)
        return self._default_response_handler(response)
