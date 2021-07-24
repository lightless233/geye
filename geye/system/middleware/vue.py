#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    vue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from django.shortcuts import render


class VueMiddleware:

    def __init__(self, get_response):
        super(VueMiddleware, self).__init__()
        self.get_response = get_response

    def __call__(self, request):
        print(dir(request))
        print(request.path)

        if request.path.startswith("/api/"):
            return self.get_response(request)
        else:
            return render(request, "index.html")
