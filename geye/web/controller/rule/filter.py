#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.rule.filter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    filter 相关的路由

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import json

from django.http import JsonResponse
from django.views import View

from geye.utils.log import logger
from geye.utils.validator import RequestValidator
from geye.utils.convert import CommonConvert
from geye.database.models import GeyeSearchRuleModel, GeyeFilterRuleModel


class AddFilterRuleView(View):
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
        args = result.params

        parent_id = args.get("id", None)
        # 检查parent_id是否存在
        if not GeyeSearchRuleModel.instance.is_exist_by_pk(parent_id):
            return JsonResponse({"code": 1003, "message": "搜索规则ID不存在!"})

        name = args.get("name")
        if not name:
            return JsonResponse({"code": 1003, "message": "规则名称有误!"})

        rule_type = CommonConvert.ensure_int(args.get("ruleType", 1))
        if rule_type not in (1, 2):
            return JsonResponse({"code": 1005, "message": "ruleType有误!"})

        rule_engine = CommonConvert.ensure_int(args.get("ruleEngine", 1))
        if rule_engine not in (1, 2):
            return JsonResponse({"code": 1006, "message": "ruleEngine有误!"})

        rule_content = args.get("ruleContent", "")

        status = CommonConvert.ensure_int(args.get("status", 1))
        if status not in (1, 0):
            return JsonResponse({"code": 1007, "message": "status有误!"})

        # action
        action = CommonConvert.ensure_int(args.get("action", 1))
        if action not in range(1, 6):
            return JsonResponse({"code": 1007, "message": "action有误!"})

        # position
        position = CommonConvert.ensure_int(args.get("position", 1))
        if position not in range(1, 6):
            return JsonResponse({"code": 1008, "message": "position有误!"})

        # priority
        priority = CommonConvert.ensure_int(args.get("priority", 5))
        if priority not in range(0, 11):
            return JsonResponse({"code": 1009, "message": "priority有误!"})

        # insert db
        obj = GeyeFilterRuleModel.instance.create(
            name=name, rule_type=rule_type, rule_engine=rule_engine, rule=rule_content,
            status=status, parent_id=parent_id, action=action, position=position, priority=priority
        )
        if obj:
            new_obj = {
                "id": obj.id,
                "name": obj.name,
                "ruleType": obj.rule_type,
                "ruleEngine": obj.rule_engine,
                "rule": obj.rule,
                "status": obj.status,
                "parentId": obj.parent_id,
                "action": obj.action,
                "position": obj.position,
                "priority": obj.priority
            }
            return JsonResponse({"code": 1001, "message": "添加成功!", "data": new_obj})
        else:
            return JsonResponse({"code": 1002, "message": "添加失败!"})


class DeleteFilterRuleView(View):
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))
        frid = json.loads(request.body).get("id", None)

        if not frid:
            return JsonResponse({"code": 1004, "message": "规则ID有误!"})

        if not GeyeFilterRuleModel.instance.is_exist(frid):
            return JsonResponse({"code": 1003, "message": "规则ID不存在!"})

        if GeyeFilterRuleModel.instance.fake_delete(frid):
            return JsonResponse({"code": 1001, "message": "删除成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "删除失败!"})


class GetFilterRuleDetailView(View):
    @staticmethod
    def get(request):
        frid = request.GET.get("id", None)
        if not frid:
            return JsonResponse({"code": 1004, "message": "规则ID有误!"})

        obj = None


