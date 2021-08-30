#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import json
from typing import Iterable

from django.http import HttpRequest
from django.views import View

from geye.constant import ResponseCode


class GeyeResponse(object):
    """
    Geye返回的数据结构
    """

    def __init__(self):
        self.code = -1
        self.message = ""
        self.data = None

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


class RequestData:
    """
    Geye 验证请求数据的结果
    """

    def __init__(self):
        self.has_error: bool = True
        self.error_message: str = ""
        self.params: dict = {}


class RequestValidator:

    # noinspection DuplicatedCode
    @staticmethod
    def check_params(request: HttpRequest, check_params: Iterable[str], method="POST_JSON",
                     check_empty=False) -> RequestData:

        rv = RequestData()

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


class BaseView(View):

    @staticmethod
    def quick_error(error_type: ResponseCode, message: str):
        resp = GeyeResponse()
        resp.data = None
        resp.code = error_type
        resp.message = message
        return resp
