#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.rules.filter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    FilterRule 过滤规则
    用于对搜索到的代码进行精确匹配

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models

from ..base import GeyeBaseModel


class GeyeFilterRuleModel(GeyeBaseModel):
    """
    用于获取详细代码后二次匹配用到的filter规则
    Filter Rule

﻿    name
        规则标题，用于区分这个规则是干啥的
    rule_type
        规则类型 1-正向匹配，2-反向匹配
    rule_engine
        1 - 正则匹配
        2 - 字符串匹配
    rule
        规则内容，正则表达式 或 需要匹配的字符串
    status
        规则状态，1-启用，0-关闭
    parent_id
        父规则（搜索规则）ID，如果这个值为0，那么该规则为全局规则，对所有search rule生效
    action
        如果rule_type为1，则这里是命中后的操作
        如果rule_type为2，则这里是未命中后的操作
            1-啥也不做，继续下一条匹配，不保存，可以用于其他规则的前置
            2-设为误报，结束匹配，可以排除掉一定不是敏感信息泄露的内容
            3-设为确认，结束匹配，保存，确定规则
            4-啥也不做（设为待确认），结束匹配，保存
    position
        决定在哪里执行二次过滤
        1-author
        2-repo name
        3-path
        4-code
        5-filename
    priority
        规则优先级，决定了规则的匹配顺序
    """

    class Meta:
        db_table = "geye_filter_rule"

    name = models.CharField(max_length=128)
    rule_type = models.PositiveSmallIntegerField(default=0)
    rule = models.TextField()
    status = models.PositiveSmallIntegerField(default=1)
    parent_id = models.BigIntegerField(default=0)
    action = models.PositiveSmallIntegerField(default=1)
    position = models.PositiveSmallIntegerField(default=1)
    priority = models.PositiveIntegerField(default=5)
