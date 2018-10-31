#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.rule.search
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    search rule相关的接口

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.views import View
from django.http import JsonResponse

from geye.database.models import GeyeSearchRuleModel


class ListSearchRuleView(View):
    """
    返回所有的search rule
    """
    @staticmethod
    def get(request):

        results = []
        rows = GeyeSearchRuleModel.instance.get_all_search_rules()
        for row in rows:
            results.append({
                "name": row.name,
                "rule": row.rule,
                "status": row.status,
                "priority": row.priority,
                "last_refresh_time": row.last_refresh_time,
                "delay": row.delay,
                "need_notification": row.need_notification,
                "clone": row.clone,
                "created_time": row.created_time
            })

        return JsonResponse({
            "code": 1001,
            "message": "success",
            "data": results
        })
