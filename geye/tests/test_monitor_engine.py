#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    test_monitor_engine
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2018 lightless. All rights reserved
"""

import sys
import os

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geye.settings")

import django
django.setup()

from geye.application import GeyeApplication
from geye.database.models.monitorRules import MonitorTaskTypeConstant, MonitorEventTypeConstant
from geye.utils.datatype import PriorityTask


if __name__ == '__main__':
    app = GeyeApplication("test")
    app.start(queues=["monitor_task_queue"], engines=["monitor_refresh_engine", "monitor_engine"])

    app.MessageQueues.MONITOR_TASK_QUEUE.put(PriorityTask(5, {
        "task_type": MonitorTaskTypeConstant.USER,
        "event_type": MonitorEventTypeConstant.PUSH_EVENT,
        "rule_content": '{"username": "lightless233"}',
    }))

