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

from geye.utils.log import logger


class CSRFTokenView(View):

    @staticmethod
    def get(request):
        logger.debug("COOKIES: {}".format(request.COOKIES))
        # csrf_token = "22222"
        csrf_token = django.middleware.csrf.get_token(request)
        response = HttpResponse(csrf_token)
        # response.set_cookie("csrftoken", csrf_token, domain="192.168.62.129", samesite=None)

        return response
