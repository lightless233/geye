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

from django.urls import path

from .controller.rule import search, filter, globalFilter


# 总的路由
# http://example.com/api/v1/rule/search/v1/all

# api下的总路由
urlpatterns = [
    # search rule URL
    path("v1/rule/search/all", search.ListSearchRuleView.as_view()),
    path("v1/rule/search/new", search.AddSearchRuleView.as_view()),
    path("v1/rule/search/delete", search.DeleteSearchRuleView.as_view()),
    path("v1/rule/search/change_status", search.ChangeStatusSearchRuleView.as_view()),
    path("v1/rule/search/get_detail", search.GetDetailView.as_view()),
    path("v1/rule/search/update", search.UpdateSearchRuleView.as_view()),

    # filter rule URL
    path("v1/rule/filter/new", filter.AddFilterRuleView.as_view()),
    path("v1/rule/filter/delete", filter.DeleteFilterRuleView.as_view()),
    path("v1/rule/filter/detail", filter.GetFilterRuleDetailView.as_view()),
    path("v1/rule/filter/update", filter.UpdateFilterRuleView.as_view()),

    # global filter rule
    path("v1/rule/global/all", globalFilter.AllGlobalFilterRulesView.as_view()),
    path("v1/rule/global/new", globalFilter.AddGlobalFilterRuleView.as_view()),
]
