#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.monitor.monitorRefresh
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    定时产生刷新任务，监控时间粒度从规则配置中获取

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2018 lightless. All rights reserved
"""
import datetime
from typing import List

import queue

from geye.core.engine.base import SingleThreadEngine
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger
from geye.database.models import GeyeMonitorRules


class MonitorRefreshEngine(SingleThreadEngine):

    def __init__(self, app_ctx, name=None):
        super(MonitorRefreshEngine, self).__init__(app_ctx, name)

        self._monitor_task_queue = self.app_ctx.MessageQueues.MONITOR_TASK_QUEUE

    def __running(self):
        return self.status == self.EngineStatus.RUNNING

    def _worker(self):
        logger.info("{name} start!".format(name=self.name))

        while self.__running():
            logger.debug("start build monitor task.")

            rows: List[GeyeMonitorRules] = GeyeMonitorRules.instance.get_all()
            current_time = datetime.datetime.now()

            for _row in rows:
                interval = _row.interval
                if _row.last_fetch_time + datetime.timedelta(minutes=interval) < current_time:
                    task = PriorityTask(_row.priority, {
                        "task_type": _row.task_type,
                        "event_type": _row.event_type,
                        "rule_content": _row.rule_content,
                    })
                    logger.debug("Create monitor task: {task}".format(task=task))
                    while self.__running():
                        try:
                            self._monitor_task_queue.put_nowait(task)
                            break
                        except queue.Full:
                            self.ev.wait(3)
                            continue

                    # 更新rule的最后刷新时间
                    _row.last_fetch_time = current_time
                    _row.save()

        logger.info("{name} stop!".format(name=self.name))
