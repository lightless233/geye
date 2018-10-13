#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

    ~~~~~~~~~~~~~~~~~~


    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models

from ..base import GeyeBaseModel


class GeyeSearchRuleModel(GeyeBaseModel):
    """
    用于搜索代码的搜索规则
    Search Rule

    name
        规则名称
    rule
        搜索关键字
    status
        状态，1-启用，0-关闭
    last_refresh_time
        上次刷新时间
    delay
        刷新间隔，单位分钟
    need_notification
        当该条SRID命中后是否需要发送通知，默认
    """

    class Meta:
        db_table = "geye_search_rule"

    name = models.CharField(max_length=128, default="", null=False)
    rule = models.CharField(max_length=1024, default="", null=False)
    status = models.PositiveSmallIntegerField(default=1)
    last_refresh_time = models.DateTimeField(auto_now_add=True)
    delay = models.PositiveIntegerField(default=5)
    need_notification = models.BooleanField(default=False)
    clone = models.BooleanField(default=False)
