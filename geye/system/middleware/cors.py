#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.system.middleware.cors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    CORS中间件，暂时把允许的domain写死到代码里，方便开发

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from urllib.parse import urlparse

from django.http import HttpResponseForbidden

from geye.utils.log import logger


class CORSMiddleware:

    def __init__(self, get_response):
        super(CORSMiddleware, self).__init__()
        self.get_response = get_response

        self.allowed_origins = [
            "localhost",
            "127.0.0.1",
        ]

    def __call__(self, request):
        response = self.get_response(request)
        logger.debug("COOKIES: {}".format(request.COOKIES))
        logger.debug("HEADERS: {}".format(request))

        origin = request.META.get("HTTP_ORIGIN", None)
        # print(origin)
        if origin:
            o = urlparse(origin)
            # print(o.hostname)
            if o.hostname in self.allowed_origins:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
                response["Access-Control-Allow-Credentials"] = "true"
                return response
            else:
                return HttpResponseForbidden("<h1>Invalid Origin</h1>")

        return response
