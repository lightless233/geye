#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.urls
    ~~~~~~~~~~~~~


    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


from django.urls import path, include

from .controller.rule import search


# 总的路由
# http://example.com/api/v1/rule/search/v1/all

# api下的总路由
urlpatterns = [
    path("v1/rule/search/all/", search.ListSearchRuleView)
]
