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
from django.db.models import F
from django.db import transaction

from geye.utils.log import logger
from ..base import GeyeBaseModel


class SearchRuleConvert:
    @staticmethod
    def convert_status(status: int, html_template="<el-tag type=\"{t}\">{c}</el-tag>"):
        if status == 1:
            return html_template.format(t="success", c="开启") if html_template else "开启"
        elif status == 0:
            return html_template.format(t="danger", c="关闭") if html_template else "关闭"
        else:
            return html_template.format(t="", c="未知") if html_template else "未知"


class SearchRuleManager(models.Manager):
    def get_all_search_rules(self):
        """
        获取所有的search rule
        """
        return self.filter(is_deleted=0).order_by("id").all()

    def is_exist(self, rule_name):
        """
        判断rule name对应的规则是否存在
        :param rule_name:
        :return:
        """
        # logger.debug("rule name: {}, exist: {}".format(rule_name, self.filter(is_deleted=0, name=rule_name).first()))
        return True if self.filter(is_deleted=0, name=rule_name).first() else False

    def is_exist_by_pk(self, pk):
        return True if self.filter(is_deleted=0, id=pk).first() else False

    def fake_delete(self, pk=None, rule_name=None):
        if pk:
            return self.filter(is_deleted=0, id=pk).update(is_deleted=1)
        if rule_name:
            return self.filter(is_deleted=0, name=rule_name).update(is_deleted=1)

        return None

    def change_status(self, pk=None, rule_name=None):
        with transaction.atomic():
            if pk:
                obj = self.select_for_update().filter(is_deleted=0, id=pk)
            elif rule_name:
                obj = self.select_for_update().filter(is_deleted=0, name=rule_name)
            else:
                return None

            obj = obj.first()
            if not obj:
                return None
            obj.status = not obj.status
            obj.save()

            return obj

    def get_detail(self, pk=None, rule_name=None):
        if pk:
            return self.filter(is_deleted=0, id=pk).first()
        elif rule_name:
            return self.filter(is_deleted=0, name=rule_name).first()
        else:
            return None


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
