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

from django.db import models

from .base import GeyeBaseModel


class MonitorTaskTypeConstant:
    REPO = "repo"
    ORG = "org"
    USER = "user"


class MonitorEventTypeConstant:
    PUSH_EVENT = "push_event"
    RELEASE_EVENT = "release_event"


class MonitorRulesManager(models.Manager):
    def get_all(self):
        return self.filter(is_deleted=False).all()


class GeyeMonitorRules(GeyeBaseModel):
    """
    task_type
        任务类型，监控维度：repo, org, user
    event_type
        监控的事件类型
        目前支持：PushEvent，ReleaseEvent
    rule_content:
        监控的内容，根据task_type的不同，这里代表的含义也不同
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

    task_type = models.CharField(default="", max_length=32)
    event_type = models.CharField(default="", max_length=32)
    rule_content = models.TextField()
    status = models.BooleanField(default=True)
    interval = models.IntegerField(default=5)
    last_fetch_time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=5)

    objects = models.Manager()
    instance = MonitorRulesManager()
