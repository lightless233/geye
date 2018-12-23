#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.monitorResults
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    存储重点监控的结果

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models

from .base import GeyeBaseModel


class MonitorResultsManager(models.Manager):
    pass


class GeyeMonitorResultsModel(GeyeBaseModel):
    """
    event_id: GitHub事件的唯一ID
    event_type: GitHub的类型
    actor_url: 事件的actor，对应用户的个人页面的URL
    actor_login: actor的登录名
    actor_display_name: actor的实际显示名称
    org_url: 产生事件的org，为对应org的页面URL
    org_name: 产生事件的org的名称
    repo_url: 产生事件的repo，为对应repo的页面URL
    repo_name: 产生事件的repo名称
    content: 事件的内容，由每个事件的parser生成，格式不固定，但是均为可读字符串
    monitor_rule_id: 由哪个监控规则捕捉到的
    """

    class Meta:
        db_table = "geye_monitor_results"

    monitor_rule_id = models.BigIntegerField(default=0)
    event_id = models.BigIntegerField(default=0)
    event_type = models.CharField(default="", max_length=128)

    actor_url = models.CharField(default="", max_length=512)
    actor_login = models.CharField(default="", max_length=128)
    actor_display_name = models.CharField(default="", max_length=128)

    org_url = models.CharField(default="", max_length=512)
    org_name = models.CharField(default="", max_length=128)

    repo_url = models.CharField(default="", max_length=512)
    repo_name = models.CharField(default="", max_length=128)

    content = models.TextField()

    event_created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    instance = MonitorResultsManager()
