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


class SearchRuleManager(models.Manager):
    def get_all_search_rules(self):
        """
        获取所有的search rule
        """
        return self.filter(is_deleted=0).all()

    def is_exist(self, rule_name):
        """
        判断rule name对应的规则是否存在
        :param rule_name:
        :return:
        """
        return True if self.filter(is_deleted=0, name=rule_name).first() else False


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
    priority:
        优先级，默认为5,1-10，越大越优先被搜索
    last_refresh_time
        上次刷新时间
    delay
        刷新间隔，单位分钟
    need_notification
        当该条SRID命中后是否需要发送通知，默认
    clone:
        当命中规则后，是否需要clone保存代码
    """

    class Meta:
        db_table = "geye_search_rule"

    name = models.CharField(max_length=128, default="", null=False)
    rule = models.CharField(max_length=1024, default="", null=False)
    status = models.PositiveSmallIntegerField(default=1)
    priority = models.PositiveIntegerField(default=5, null=False)
    last_refresh_time = models.DateTimeField(auto_now_add=True)
    delay = models.PositiveIntegerField(default=5)
    need_notification = models.BooleanField(default=False)
    clone = models.BooleanField(default=False)

    object = models.Manager()
    instance = SearchRuleManager()
