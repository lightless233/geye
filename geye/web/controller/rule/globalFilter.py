#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.rule.global
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    global filter rule 相关的controller

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import json

from django.http import JsonResponse
from django.views import View

from geye.database.models import GeyeFilterRuleModel
from geye.utils.convert import CommonConvert
from geye.utils.log import logger
from geye.utils.validator import RequestValidator


class AllGlobalFilterRulesView(View):
    @staticmethod
    def get(request):
        rows = GeyeFilterRuleModel.instance.all_global_filter_rule()
        logger.debug("rows: {}".format(rows))
        data = []
        for row in rows:
            data.append({
                "id": row.id,
                "name": row.name,
                "ruleType": row.rule_type,
                "ruleEngine": row.rule_engine,
                "ruleContent": row.rule,
                "status": row.status,
                "parentId": row.parent_id,
                "action": row.action,
                "position": row.position,
                "priority": row.priority,
            })
        return JsonResponse({"code": 1001, "message": "获取成功!", "data": data})


class AddGlobalFilterRuleView(View):
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))

        # 检查参数是否为空
        result = RequestValidator.check_params(
            request, check_empty=True,
            check_params=["name", "ruleType", "ruleEngine",
                          "ruleContent", "status", "action", "position", "priority"]
        )
        if result.has_error:
            logger.error("error: {}".format(result.error_message))
            return JsonResponse({"code": 1004, "message": result.error_message})
        params = result.params

        name = params.get("name")
        if not name:
            return JsonResponse({"code": 1003, "message": "规则名称有误!"})

        rule_type = CommonConvert.ensure_int(params.get("ruleType", 1))
        if rule_type not in (1, 2):
            return JsonResponse({"code": 1005, "message": "ruleType有误!"})

        rule_engine = CommonConvert.ensure_int(params.get("ruleEngine", 1))
        if rule_engine not in (1, 2):
            return JsonResponse({"code": 1006, "message": "ruleEngine有误!"})

        rule_content = params.get("ruleContent", "")
        if not rule_content:
            return JsonResponse({"code": 1004, "message": "ruleContent不能为空"})

        status = CommonConvert.ensure_int(params.get("status", 1))
        if status not in (1, 0):
            return JsonResponse({"code": 1007, "message": "status有误!"})

        # action
        action = CommonConvert.ensure_int(params.get("action", 1))
        if action not in range(1, 6):
            return JsonResponse({"code": 1007, "message": "action有误!"})

        # position
        position = CommonConvert.ensure_int(params.get("position", 1))
        if position not in range(1, 6):
            return JsonResponse({"code": 1008, "message": "position有误!"})

        # priority
        priority = CommonConvert.ensure_int(params.get("priority", 5))
        if priority not in range(0, 11):
            return JsonResponse({"code": 1009, "message": "priority有误!"})

        obj = GeyeFilterRuleModel.instance.create(
            name=name, rule_type=rule_type, rule_engine=rule_engine, rule=rule_content,
            status=status, parent_id=0, action=action, position=position, priority=priority
        )
        if obj:
            return JsonResponse({"code": 1001, "message": "添加成功!", "data": {
                "id": obj.id,
                "name": obj.name,
                "ruleType": obj.rule_type,
                "ruleEngine": obj.rule_engine,
                "ruleContent": obj.rule,
                "status": obj.status,
                "parentId": obj.parent_id,
                "action": obj.action,
                "position": obj.position,
                "priority": obj.priority
            }})
        else:
            return JsonResponse({"code": 1002, "message": "添加失败!"})


class DeleteGlobalFilterRuleView(View):
    @staticmethod
    def post(request):
        # frid = request.POST.get("id", None)
        frid = json.loads(request.body).get("id", None)
        logger.debug("frid: {}".format(frid))
        if not frid or not GeyeFilterRuleModel.instance.is_exist_global(frid):
            return JsonResponse({"code": 1004, "message": "规则ID不存在!"})

        if GeyeFilterRuleModel.instance.fake_delete_global(frid):
            return JsonResponse({"code": 1001, "message": "删除成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "删除失败!"})


class GetDetailView(View):
    @staticmethod
    def get(request):
        frid = request.GET.get("id", None)
        if not frid or not GeyeFilterRuleModel.instance.is_exist_global(frid):
            return JsonResponse({"code": 1004, "message": "规则ID不存在!"})

        obj = GeyeFilterRuleModel.instance.get_detail(pk=frid)
        if obj:
            return JsonResponse({"code": 1001, "message": "获取成功!", "data": {
                "id": obj.id,
                "name": obj.name,
                "ruleType": obj.rule_type,
                "ruleEngine": obj.rule_engine,
                "ruleContent": obj.rule,
                "status": obj.status,
                "parentId": obj.parent_id,
                "action": obj.action,
                "position": obj.position,
                "priority": obj.priority
            }})
        else:
            return JsonResponse({"code": 1002, "message": "获取失败!"})


class UpdateGlobalFilterRuleView(View):
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))

        # 检查参数是否为空
        result = RequestValidator.check_params(
            request, check_empty=True,
            check_params=["id", "name", "ruleType", "ruleEngine",
                          "ruleContent", "status", "action", "position", "priority"]
        )
        if result.has_error:
            logger.error("error: {}".format(result.error_message))
            return JsonResponse({"code": 1004, "message": result.error_message})
        params = result.params

        if not GeyeFilterRuleModel.instance.is_exist_global(pk=params.get("id", None)):
            return JsonResponse({"code": 1004, "message": "规则ID不存在!"})

        name = params.get("name")
        if not name:
            return JsonResponse({"code": 1003, "message": "规则名称有误!"})

        rule_type = CommonConvert.ensure_int(params.get("ruleType", 1))
        if rule_type not in (1, 2):
            return JsonResponse({"code": 1005, "message": "ruleType有误!"})

        rule_engine = CommonConvert.ensure_int(params.get("ruleEngine", 1))
        if rule_engine not in (1, 2):
            return JsonResponse({"code": 1006, "message": "ruleEngine有误!"})

        rule_content = params.get("ruleContent", "")
        if not rule_content:
            return JsonResponse({"code": 1004, "message": "ruleContent不能为空"})

        status = CommonConvert.ensure_int(params.get("status", 1))
        if status not in (1, 0):
            return JsonResponse({"code": 1007, "message": "status有误!"})

        # action
        action = CommonConvert.ensure_int(params.get("action", 1))
        if action not in range(1, 6):
            return JsonResponse({"code": 1007, "message": "action有误!"})

        # position
        position = CommonConvert.ensure_int(params.get("position", 1))
        if position not in range(1, 6):
            return JsonResponse({"code": 1008, "message": "position有误!"})

        # priority
        priority = CommonConvert.ensure_int(params.get("priority", 5))
        if priority not in range(0, 11):
            return JsonResponse({"code": 1009, "message": "priority有误!"})

        obj = GeyeFilterRuleModel.instance.update_filter_rule(params)
        if not obj:
            return JsonResponse({"code": 1002, "message": "更新失败!"})
        else:
            return JsonResponse({"code": 1001, "message": "更新成功!", "data": {
                "id": obj.id,
                "name": obj.name,
                "ruleType": obj.rule_type,
                "ruleEngine": obj.rule_engine,
                "ruleContent": obj.rule,
                "status": obj.status,
                "parentId": obj.parent_id,
                "action": obj.action,
                "position": obj.position,
                "priority": obj.priority
            }})
