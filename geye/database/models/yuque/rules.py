#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    rules
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from django.db import models

from geye.database.models.base import GeyeBaseModel


class GeyeYuqueSearchRuleManger(models.Manager):

    def all_enable_rules(self):
        """
        获取所有开启的语雀监控规则
        :return:
        """
        return self.filter(is_deleted=0, status=1).order_by("-priority").all()


class GeyeYuqueSearchRuleModel(GeyeBaseModel):
    """
    语雀监控关键词规则
    """

    class Meta:
        db_table = "geye_yuque_search_rule"

    # 规则名称
    name = models.CharField(max_length=128, default="", null=False)

    # 规则内容，即要搜索的关键字
    rule = models.CharField(max_length=1024, default="", null=False)

    # 规则状态
    # 0 - 关闭
    # 1 - 启用
    status = models.PositiveSmallIntegerField(default=1, null=False)

    # 优先级，默认为5，可选值：1-10
    # 越大优先级越高
    priority = models.PositiveIntegerField(default=5, null=False)

    # 上一次刷新时间
    last_refresh_time = models.DateTimeField(auto_now_add=True, null=False)

    # 刷新间隔，单位：分钟
    interval = models.PositiveIntegerField(default=5, null=False)

    # 命中后是否需要发消息通知
    # 0 - 不通知
    # 1 - 通知
    need_notification = models.PositiveSmallIntegerField(default=0, null=False)

    # 命中后是否需要将内容存储下来
    need_save = models.BooleanField(default=False, null=False)

    objects = models.Manager()
    instance = GeyeYuqueSearchRuleManger()
