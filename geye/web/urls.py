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


# search rule下的路由
search_rule_urlpatterns = [
    path("v1/all/", search.ListSearchRuleView),
]

# api下的总路由
urlpatterns = [
    path("rule/search/", include(search_rule_urlpatterns)),
]
