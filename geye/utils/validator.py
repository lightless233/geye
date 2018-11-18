#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.utils.validator
    ~~~~~~~~~~~~~~~~~~~~

    一些简单的通用验证器

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import json
from typing import List

from django.http import HttpRequest


class RequestValidatorResult:
    def __init__(self):
        self.has_error: bool = True
        self.error_message: str = ""
        self.params: dict = ""


class RequestValidator:
    @staticmethod
    def check_params(
            request: HttpRequest,
            check_params: List[str],
            method="POST_JSON",
            check_empty=False) -> RequestValidatorResult:
        # rv = {"has_error": True, "error_message": "", "params": None}
        rv = RequestValidatorResult()

        # 获取传递来的参数
        if method == "POST_JSON":
            request_data = json.loads(request.body)
        elif method == "GET_DATA":
            request_data = request.GET
        elif method == "POST_DATA":
            request_data = request.POST
        else:
            rv.error_message = "method有误，只能为'POST_JSON', 'GET_DATA', 'POST_DATA'中的一种."
            return rv

        # 开始检查
        request_keys = request_data.keys()
        for key_name in check_params:
            # 1. 检查这个参数是否发送过来了
            if key_name not in request_keys:
                rv.error_message = "'{}'参数不存在".format(key_name)
                return rv
            # 2. 检查这个变量对应的值是否为空
            if check_empty:
                if request_data.get(key_name, None) is None:
                    rv.error_message = "'{}'参数的值为空".format(key_name)
                    return rv

        # 检查完了
        rv.has_error = False
        rv.params = request_data
        return rv
