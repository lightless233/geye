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
import json

from django.views import View
from django.http import JsonResponse, HttpRequest

from geye.database.models import GeyeSearchRuleModel, GeyeFilterRuleModel
from geye.utils.convert import CommonConvert
from geye.utils.log import logger
from geye.utils.validator import RequestValidator


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
                "id": row.id,
                "rule_name": row.name,
                "rule_content": row.rule,
                "status": row.status,
                "priority": row.priority,
                "last_refresh_time": CommonConvert.datetime_to_str(row.last_refresh_time),
                "delay": row.delay,
                "need_notification": row.need_notification,
                "clone": row.clone,
                "created_time": CommonConvert.datetime_to_str(row.created_time),
                "updated_time": CommonConvert.datetime_to_str(row.updated_time),
            })

        return JsonResponse({
            "code": 1001,
            "message": "success",
            "data": results
        })


class AddSearchRuleView(View):
    """
    添加一条search rule
    """

    @staticmethod
    def post(request: HttpRequest):
        logger.debug("POST: {}".format(request.body))
        r_json = {
            "code": 1001,
            "message": "",
            "data": ""
        }

        # 简单的检查参数是否为空
        result = RequestValidator.check_params(
            request,
            ["ruleName", "ruleContent", "status", "defaultFilter", "delay", "priority", "notification", "clone"],
            check_empty=True
        )
        logger.debug("check result: {}".format(result))
        if result.has_error:
            r_json["code"] = 1004
            r_json["message"] = result.error_message
            logger.error("error_message: {}".format(result.error_message))
            return JsonResponse(r_json)
        request_data = result.params

        rule_name = request_data.get("ruleName")
        rule_content = request_data.get("ruleContent")

        # 检查rule name是否存在
        if GeyeSearchRuleModel.instance.is_exist(rule_name):
            r_json["code"] = 1002
            r_json["message"] = "规则名称已存在!"
            return JsonResponse(r_json)

        status = request_data.get("status", 0)
        default_filter = request_data.get("defaultFilter", 1)
        default_filter = int(default_filter)
        delay: str = request_data.get("delay", "30")
        priority: str = request_data.get("priority", "5")

        # 检查优先级和delay
        if isinstance(priority, str) and not priority.isdigit():
            r_json["code"] = 1003
            r_json["message"] = "非法的优先级!"
            return JsonResponse(r_json)
        if isinstance(delay, str) and not delay.isdigit():
            r_json["code"] = 1003
            r_json["message"] = "非法的搜索间隔时间!"

        # 通知 和 auto-clone功能暂不开启
        notification = 0
        clone = 0

        # 插入到数据库中
        obj = GeyeSearchRuleModel.instance.create(
            name=rule_name, rule=rule_content, status=status, priority=priority, last_refresh_time=None,
            delay=delay, need_notification=notification, clone=clone
        )

        # 如果default filter 为 true，则插入默认规则
        if default_filter:
            # 默认filter为：
            #   如果没有匹配到搜索的关键词，则结束匹配
            GeyeFilterRuleModel.instance.create(
                name="DefaultFilter", rule_type=2, rule_engine=2,
                rule=rule_content, status=1, parent_id=obj.id, action=2,
                position=4, priority=10
            )

        r_json["code"] = 1001
        r_json["message"] = "创建成功!"
        r_json["data"] = obj.id
        return JsonResponse(r_json)


class ChangeStatusSearchRuleView(View):
    @staticmethod
    def post(request):
        srid = json.loads(request.body).get("id", None)
        if not srid:
            return JsonResponse({"code": 1004, "message": "规则id有误!"})
        if not GeyeSearchRuleModel.instance.is_exist_by_pk(srid):
            return JsonResponse({"code": 1003, "message": "规则id不存在!"})

        if not GeyeSearchRuleModel.instance.change_status(pk=srid):
            return JsonResponse({"code": 1002, "message": "切换规则状态!"})
        else:
            return JsonResponse({"code": 1001, "message": "切换规则状态成功!"})


class DeleteSearchRuleView(View):
    @staticmethod
    def post(request):
        srid = json.loads(request.body).get("id", None)
        logger.debug("srid: {}".format(srid))
        # logger.debug("request body: {}".format(json.loads(request.body)))
        if not srid:
            return JsonResponse({"code": 1004, "message": "规则id有误!"})

        if not GeyeSearchRuleModel.instance.is_exist_by_pk(srid):
            return JsonResponse({"code": 1003, "message": "规则id不存在!"})

        if not GeyeSearchRuleModel.instance.fake_delete(pk=srid):
            return JsonResponse({"code": 1002, "message": "删除失败!"})
        else:
            return JsonResponse({"code": 1001, "message": "删除成功!"})


class GetDetailView(View):
    @staticmethod
    def get(request):
        srid = request.GET.get("id", None)
        rule_name = request.GET.get("rule_name", None)
        logger.debug("srid: {}, rule_name: {}".format(srid, rule_name))
        if not srid and not rule_name:
            return JsonResponse({"code": 1004, "message": "id和rule_name均有误"})

        search_rule_obj = GeyeSearchRuleModel.instance.get_detail(pk=srid, rule_name=rule_name)
        if not search_rule_obj:
            return JsonResponse({"code": 1003, "message": "规则不存在!"})

        # filter_rule_obj = GeyeFilterRuleModel.instance.get_filter_rules_by_srid(srid, contains_global_rule=False)
        filter_rule_obj = GeyeFilterRuleModel.instance.filter(is_deleted=0, parent_id=srid).order_by("-priority").all()

        rv = {
            "search_rule": {
                "ruleName": search_rule_obj.name,
                "ruleContent": search_rule_obj.rule,
                "status": search_rule_obj.status,
                "priority": search_rule_obj.priority,
                "delay": search_rule_obj.delay,
                "needNotification": int(search_rule_obj.need_notification),
                "clone": int(search_rule_obj.clone),
            },
            "filter_rule": [{
                "id": fr.id,
                "name": fr.name,
                "ruleType": fr.rule_type,
                "ruleEngine": fr.rule_engine,
                "ruleContent": fr.rule,
                "status": fr.status,
                "parentId": fr.parent_id,
                "action": fr.action,
                "position": fr.position,
                "priority": fr.priority
            } for fr in filter_rule_obj],
        }

        return JsonResponse({"code": 1001, "message": "success", "data": rv})


class UpdateSearchRuleView(View):
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))
        result = RequestValidator.check_params(
            request, check_empty=True,
            check_params=["id", "ruleName", "ruleContent", "status", "needNotification", "clone", "delay", "priority"]
        )
        if result.has_error:
            em = result.error_message
            logger.error("error_message: {}".format(em))
            return JsonResponse({"code": 1004, "message": em})

        request_data = result.params

        # 检查ID是否存在
        srid = request_data.get("id", None)
        if not srid:
            return JsonResponse({"code": 1004, "message": "规则ID有误!"})
        if not GeyeSearchRuleModel.instance.is_exist_by_pk(srid):
            return JsonResponse({"code": 1003, "message": "规则ID不存在!"})

        rule_name = request_data.get("ruleName")
        rule_content = request_data.get("ruleContent")
        status = request_data.get("status")
        delay: str = request_data.get("delay")
        priority: str = request_data.get("priority")

        if isinstance(priority, str) and not priority.isdigit():
            return JsonResponse({"code": 1003, "message": "优先级有误!"})
        if isinstance(delay, str) and not delay.isdigit():
            return JsonResponse({"code": 1003, "message": "刷新间隔有误!"})

        # str -> int
        delay = int(delay) if isinstance(delay, str) else delay
        priority = int(priority) if isinstance(priority, str) else priority

        need_notification = 0
        clone = 0

        # update db
        obj = GeyeSearchRuleModel.instance.filter(is_deleted=0, id=srid).update(
            name=rule_name, rule=rule_content, status=status,
            priority=priority, delay=delay, need_notification=need_notification, clone=clone
        )

        if obj:
            return JsonResponse({"code": 1001, "message": "更新规则成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "更新规则失败!"})
