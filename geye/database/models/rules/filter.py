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

from django.db import models, transaction

from ..base import GeyeBaseModel


class FilterRuleManager(models.Manager):
    def get_filter_rules_by_srid(self, srid, contains_global_rule=True) -> list:
        """
        返回指定SRID对应的全部filter规则
        :param srid:
        :param contains_global_rule: True-包含全局规则，False-不包含全局规则
        :return: list
        """
        all_rules = []
        if contains_global_rule:
            global_rules = self.filter(is_deleted=0, parent_id=0, status=1).order_by('-priority').all()
            for r in global_rules:
                all_rules.append(r)

        child_rules = self.filter(is_deleted=0, parent_id=srid, status=1).order_by('-priority').all()
        for r in child_rules:
            all_rules.append(r)
        return all_rules

    def is_exist(self, pk):
        return self.filter(is_deleted=0, id=pk).first()

    def is_exist_global(self, pk):
        return self.filter(is_deleted=0, parent_id=0, id=pk).first()

    def fake_delete(self, pk):
        return self.filter(is_deleted=0, id=pk).update(is_deleted=1)

    def fake_delete_global(self, pk):
        return self.filter(is_deleted=0, id=pk, parent_id=0).update(is_deleted=1)

    def get_detail(self, pk):
        return self.filter(is_deleted=0, id=pk).first()

    def get_detail_global(self, pk):
        return self.filter(is_deleted=0, id=pk, parent_id=0).first()

    def update_filter_rule(self, params: dict) -> "GeyeFilterRuleModel":
        with transaction.atomic():
            obj: GeyeFilterRuleModel = self.select_for_update().filter(is_deleted=0, id=params.get("id")).first()
            obj.name = params.get("name")
            obj.rule = params.get("ruleContent")
            obj.rule_type = params.get("ruleType")
            obj.rule_engine = params.get("ruleEngine")
            obj.status = params.get("status")
            obj.action = params.get("action")
            obj.position = params.get("position")
            obj.priority = params.get("priority")

            obj.save()
            return obj

    def all_global_filter_rule(self):
        return self.filter(is_deleted=0, parent_id=0).all()

    def get_name_by_pk(self, pk):
        obj = self.filter(is_deleted=0, id=pk).first()
        if not obj:
            return ""
        else:
            return obj.name


class GeyeFilterRuleModel(GeyeBaseModel):
    """
    用于获取详细代码后二次匹配用到的filter规则
    Filter Rule

    name
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
            2-设为误报，结束匹配，不保存，可以排除掉一定不是敏感信息泄露的内容
            3-设为误报，结束匹配，保存，可以排除掉一定不是敏感信息泄露的内容
            4-设为确认，结束匹配，保存，确定规则
            5-啥也不做（设为待确认），结束匹配，保存
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
    rule_engine = models.PositiveSmallIntegerField(default=0)
    rule = models.TextField()
    status = models.PositiveSmallIntegerField(default=1)
    parent_id = models.BigIntegerField(default=0)
    action = models.PositiveSmallIntegerField(default=1)
    position = models.PositiveSmallIntegerField(default=1)
    priority = models.PositiveIntegerField(default=5)

    objects = models.Manager()
    instance = FilterRuleManager()

    def __str__(self):
        return "<GeyeFilterRuleModel id:{} name:{} parent_id: {}>".format(self.id, self.name, self.parent_id)

    def __repr__(self):
        return "<GeyeFilterRuleModel id:{} name:{} parent_id: {}>".format(self.id, self.name, self.parent_id)
