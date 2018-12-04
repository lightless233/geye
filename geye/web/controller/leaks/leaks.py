#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.leaks.leaks
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Leaks相关的controller

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import json

from django.http import JsonResponse
from django.views import View

from geye.database.models import GeyeLeaksModel, GeyeSearchRuleModel, GeyeFilterRuleModel, LeaksStatusConstant


class AllLeaksView(View):
    PAGE_SIZE = 20

    def get(self, request):
        page = request.GET.get("page", 1)
        status = request.GET.get("status", None)
        if not status:
            return JsonResponse({"code": 1005, "message": "参数错误!"})

        page = int(page)
        status = status.split(",")
        if not status:
            status = [1, 2, 3]

        if not page or not status:
            return JsonResponse({"code": 1004, "message": "参数错误!"})

        start_id = (page - 1) * self.PAGE_SIZE
        end_id = start_id + self.PAGE_SIZE

        sql = GeyeLeaksModel.instance.filter(
            is_deleted=0, status__in=status
        ).order_by("-created_time")

        rows = sql[start_id:end_id]
        total_count = sql.count()

        data = []
        for row in rows:
            search_rule_name = GeyeSearchRuleModel.instance.get_name_by_pk(row.srid)
            filter_rule_name = GeyeFilterRuleModel.instance.get_name_by_pk(row.frid)
            if not filter_rule_name:
                filter_rule_name = "规则已删除"
            data.append({
                "id": row.id,
                "repoName": row.repo_name,
                "author": row.author,
                "path": row.path,
                "filename": row.filename,
                "sha": row.sha,
                "full_code_url": row.full_code_url,
                "url": row.url,
                "code": row.code,
                "srid": row.srid,
                "frid": row.frid,
                "status": row.status,
                "pushed": row.pushed,
                "searchRuleName": search_rule_name,
                "filterRuleName": filter_rule_name,
                "created_time": row.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return JsonResponse({"code": 1001, "message": "获取成功!", "data": data, "total_count": total_count})


class DeleteLeakView(View):
    """
    删除一条Leaks记录
    """
    @staticmethod
    def post(request):
        leak_id = json.loads(request.body).get("id", None)

        if not leak_id or not GeyeLeaksModel.instance.is_exist_by_pk(leak_id):
            return JsonResponse({"code": 1004, "message": "id不存在!"})

        if GeyeLeaksModel.instance.fake_delete(leak_id):
            return JsonResponse({"code": 1001, "message": "删除成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "删除失败!"})


class ChangeStatusLeakView(View):
    """
    修改leaks的状态
    request params:
        - action
        - id
    """
    ACTIONS = ["ignore", "confirm"]

    def post(self, request):
        request_params = json.loads(request.body)
        action = request_params.get("action", None)
        leak_id = request_params.get("id", None)
        if not action or action not in self.ACTIONS:
            return JsonResponse({"code": 1004, "message": "action不存在!"})
        if not leak_id or not GeyeLeaksModel.instance.is_exist_by_pk(leak_id):
            return JsonResponse({"code": 1004, "message": "id不存在!"})

        if action == "confirm":
            result = GeyeLeaksModel.instance.filter(is_deleted=0, pk=leak_id).update(status=LeaksStatusConstant.CONFIRM)
            if result:
                return JsonResponse({"code": 1001, "message": "修改成功!"})
            else:
                return JsonResponse({"code": 1002, "message": "修改失败!"})
        elif action == "ignore":
            result = GeyeLeaksModel.instance.filter(is_deleted=0, pk=leak_id).update(status=LeaksStatusConstant.IGNORE)
            if result:
                return JsonResponse({"code": 1001, "message": "修改成功!"})
            else:
                return JsonResponse({"code": 1002, "message": "修改失败!"})

        return JsonResponse({"code": 1003, "message": "error action!"})


class BatchChangeStatusLeakView(View):
    """
    批量修改leaks的状态
    request params:
        :action:
        :ids:
    """
    ACTIONS = ["ignore", "confirm"]

    def post(self, request):
        request_params = json.loads(request.body)
        action = request_params.get("action", None)
        leak_id = request_params.get("ids", list())

        if not action or action not in self.ACTIONS:
            return JsonResponse({"code": 1004, "message": "action不存在!"})
        if not isinstance(leak_id, list) or not len(leak_id):
            return JsonResponse({"code": 1004, "message": "id不存在!"})

        if action == "confirm":
            new_status = LeaksStatusConstant.CONFIRM
        elif action == "ignore":
            new_status = LeaksStatusConstant.IGNORE

        result = GeyeLeaksModel.instance.filter(is_deleted=0, pk__in=leak_id).update(status=new_status)
        if result:
            return JsonResponse({"code": 1001, "message": "更新成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "更新失败!"})
