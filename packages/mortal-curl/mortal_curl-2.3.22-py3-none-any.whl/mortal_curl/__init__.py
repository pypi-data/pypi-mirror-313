#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/17 10:11
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .curl_main import MortalCurlMain


class MortalCurl(MortalCurlMain):
    def to_dict(self, curl):
        return self._to_dict(curl)

    def to_python(self, curl_path: str, file_path: str):
        self._to_python(curl_path, file_path)

    def to_yaml(self, curl_path: str, file_path: str):
        self._to_yaml(curl_path, file_path)
