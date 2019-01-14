#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.monitorRules
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    存储重点监控的规则部分

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models, transaction

from .base import GeyeBaseModel


class CommonConstant:
    @classmethod
    def lst(cls):
        obj = filter(lambda i: i[0].isupper(), cls.__mro__[0].__dict__.items())
        return [x[1] for x in list(obj)]


class MonitorTaskTypeConstant(CommonConstant):
    REPO = "repo"
    ORG = "org"
    USER = "user"


class MonitorEventTypeConstant(CommonConstant):
    PUSH_EVENT = "push_event"
    RELEASE_EVENT = "release_event"


class MonitorRulesManager(models.Manager):
    def get_all(self):
        """
        获取所有的记录
        :return:
        """
        return self.filter(is_deleted=False).all()

    def is_pk_exist(self, pk):
        """
        根据主键判断对应的记录是否存在
        :param pk:
        :return:
        """
        return self.filter(is_deleted=False, pk=pk).first()

    def fake_delete_by_pk(self, pk):
        """
        根据主键删除一条规则
        :param pk: 主键ID
        :return: boolean
        """
        with transaction.atomic():
            obj: GeyeMonitorRules = self.select_for_update().filter(is_deleted=False, pk=pk).first()
            if not obj:
                return False
            else:
                obj.is_deleted = True
                obj.save()
                return True


class GeyeMonitorRules(GeyeBaseModel):
    """
    task_type
        任务类型，监控维度：repo, org, user
    event_type
        监控的事件类型
        目前支持：PushEvent，ReleaseEvent
    rule_content:
        监控的内容，根据task_type的不同，这里代表的含义也不同
        是个JSON字符串
            1. 组织监控：{"org_name": ""}
            2. 仓库监控：{"owner": "", "repo_name": ""}
            3. 用户监控：{"username": ""}
    status:
        规则状态，是否开启
    interval:
        每个仓库的监控时间间隔，单位分钟
    last_fetch_time:
        上次fetch信息的时间
    priority:
        优先级，1-10
    """

    class Meta:
        db_table = "geye_monitor_rules"

    task_type = models.CharField(default="", max_length=32, db_index=True)
    event_type = models.CharField(default="", max_length=128)
    rule_content = models.TextField()
    status = models.BooleanField(default=True)
    interval = models.IntegerField(default=5)
    last_fetch_time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=5)

    objects = models.Manager()
    instance = MonitorRulesManager()

    def convert_to_dict(self):
        return {
            "id": self.id,
            "taskType": self.task_type,
            "eventType": self.event_type,
            "ruleContent": self.rule_content,
            "status": self.status,
            "interval": self.interval,
            "priority": self.priority,
            "lastFetchTime": self.last_fetch_time,
        }
