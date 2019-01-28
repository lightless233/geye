#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.monitor.monitorSave
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    持久化存储monitor的结果

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue

from geye.core.engine.base import SingleThreadEngine
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger


class MonitorSaveEngine(SingleThreadEngine):

    def __init__(self, app_ctx, name=None):
        super(MonitorSaveEngine, self).__init__(app_ctx, name)

        self._save_queue = self.app_ctx.MessageQueues.MONITOR_SAVE_QUEUE

    def __wait(self, timeout: int):
        self.ev.wait(timeout)

    def __get_task_from_queue(self):
        """
        从队列中获取一个任务
        :return:
        """
        while self.is_running():
            try:
                task: PriorityTask = self._save_queue.get_nowait()
                return task.priority, task.data
            except queue.Empty:
                self.__wait(1)
                continue

    def _worker(self):
        logger.info("{name} start!".format(name=self.name))

        while self.is_running():
            pass

        logger.info("{name} stop!".format(name=self.name))

