#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.handlerCenter.searchResults
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    handle center相关的路由
    只有search结果的部分

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import json

from django.http import JsonResponse
from django.views import View

from geye.database.models.leaks import GeyeLeaksModel
from geye.database.models.rules import GeyeSearchRuleModel, GeyeFilterRuleModel


class AllSearchResults(View):

    PAGE_SIZE = 20

    def get(self, request):
        page = request.GET.get("page", 1)
        page = int(page)
        start_id = (page-1) * self.PAGE_SIZE
        end_id = start_id + self.PAGE_SIZE
        # 只返回待处理状态的
        rows = GeyeLeaksModel.instance.filter(is_deleted=0, status=1).order_by("-created_time")[start_id:end_id]

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

        return JsonResponse({"code": 1001, "message": "获取成功!", "data": data})


class IgnoreSearchResult(View):
    @staticmethod
    def post(request):
        leak_id = json.loads(request.body).get("id", None)
        if not leak_id or not GeyeLeaksModel.instance.is_exist_by_pk(leak_id):
            return JsonResponse({"code": 1004, "message": "leak id不存在!"})

        obj = GeyeLeaksModel.instance.filter(pk=leak_id).update(status=3)
        if obj:
            return JsonResponse({"code": 1001, "message": "已设为误报!"})
        else:
            return JsonResponse({"code": 1002, "message": "设为误报失败!"})


class ConfirmSearchResult(View):
    @staticmethod
    def post(request):
        leak_id = json.loads(request.body).get("id", None)
        if not leak_id or not GeyeLeaksModel.instance.is_exist_by_pk(leak_id):
            return JsonResponse({"code": 1004, "message": "leak id不存在!"})

        obj = GeyeLeaksModel.instance.filter(pk=leak_id).update(status=2)
        if obj:
            return JsonResponse({"code": 1001, "message": "已确认为泄露!"})
        else:
            return JsonResponse({"code": 1002, "message": "设为泄露失败!"})
