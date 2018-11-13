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
from django.http import JsonResponse, HttpRequest

from geye.database.models import GeyeSearchRuleModel, GeyeFilterRuleModel
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
        if result.get("has_error"):
            r_json["code"] = 1004
            r_json["message"] = result.get("error_message")
            logger.error("error_message: {}".format(result.get("error_message")))
            return JsonResponse(r_json)
        request_data = result.get("params")

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
