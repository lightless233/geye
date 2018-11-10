#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.system.csrf
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用于前端页面获取CSRF Token

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


from django.views import View
from django.http import HttpResponse
import django.middleware.csrf


class CSRFTokenView(View):

    @staticmethod
    def get(request):
        print(request.COOKIES)
        csrf_token = django.middleware.csrf.get_token(request)
        response = HttpResponse(csrf_token)
        # response.set_cookie(key="x-csrf-token", value=csrf_token)

        return response
