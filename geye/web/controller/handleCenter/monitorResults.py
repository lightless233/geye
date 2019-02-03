#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.handleCenter.monitorResults
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    展示监控结果

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from typing import List

from django.views import View
from django.http import JsonResponse

from geye.database.models import GeyeMonitorResultsModel


class AllMonitorResults(View):
    PAGE_SIZE = 20

    def get(self, request):
        page = request.GET.get("page", 1)
        page = int(page)
        start_id = (page - 1) * self.PAGE_SIZE
        end_id = start_id + self.PAGE_SIZE

        # 查询所有的数据
        rows: List[GeyeMonitorResultsModel] = GeyeMonitorResultsModel.instance.filter(is_deleted=0).order_by("-event_created_time")[start_id:end_id]

        return_data = []
        for row in rows:

            event_created_time = row.event_created_time.strftime("%Y-%m-%d %H:%M:%S")

            return_data.append({
                "monitor_rule_id": row.monitor_rule_id,
                "event_id": row.event_id,
                "event_type": row.event_type,
                "actor_url": row.actor_url,
                "actor_login": row.actor_login,
                "actor_display_name": row.actor_display_name,
                "org_url": row.org_url,
                "org_name": row.org_name,
                "repo_url": row.repo_url,
                "repo_name": row.repo_name,
                "content": row.content,
                "event_created_time": event_created_time,
                "id": row.id,
            })

        return JsonResponse({"code": 1001, "message": "获取成功!", "data": return_data})
