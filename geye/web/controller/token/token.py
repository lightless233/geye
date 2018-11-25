#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.web.token
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Token 相关的controller

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from django.views import View


class TokensView(View):
    """
    获取所有token信息
    """
    @staticmethod
    def get(request):
        pass


class DeleteTokenView(View):
    """
    删除某条token
    """
    @staticmethod
    def post(request):
        pass


class AddTokenView(View):
    """
    添加一条token
    """
    @staticmethod
    def post(request):
        pass


class EditTokenView(View):
    """
    编辑一条token
    """
    @staticmethod
    def post(request):
        pass


class UpdateStatus(View):
    """
    切换一条token状态
    """
    @staticmethod
    def post(request):
        pass


class TokenDetailsView(View):
    """
    获取某条token的详细信息
    """
    @staticmethod
    def get(request):
        pass
