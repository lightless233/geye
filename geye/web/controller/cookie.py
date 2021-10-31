#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    cookie
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""

from .base import BaseView


class ListCookieView(BaseView):

    @staticmethod
    def get(request):
        """
        列出所有的 cookie
        :param request:
        :return:
        """
        pass
