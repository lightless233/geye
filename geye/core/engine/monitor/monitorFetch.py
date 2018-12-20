#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.monitor.monitorFetch
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    monitor任务的监控engine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue
from django.conf import settings

from geye.core.engine.base import MultiThreadEngine
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger


class MonitorEngine(MultiThreadEngine):

    def __init__(self, app_ctx, name, pool_size=None):
        super(MonitorEngine, self).__init__(app_ctx, name, pool_size)

        # 获取配置信息
        pass

        # 获取代理信息
        self.use_proxy = settings.USE_SEARCH_PROXY
        self.proxies = settings.SEARCH_PROXIES if self.use_proxy else []

        # 获取队列信息
        self._monitor_task_queue = self.app_ctx.MessageQueues.MONITOR_TASK_QUEUE
        self._monitor_result_queue = None

    def __is_running(self):
        return self.status == self.EngineStatus.RUNNING

    def __get_task(self):
        """
        从队列中获取任务
        :return:
        """
        while self.__is_running():
            try:
                task: PriorityTask = self._monitor_task_queue.get_nowait()
                return task.priority, task.data
            except queue.Empty:
                self.ev.wait(1)
                continue
        else:
            return None, None

    def __put_task(self, priority, task):
        """
        放置任务到队列中
        :param priority:
        :param task:
        :return:
        """
        wrap_task = PriorityTask(priority, task)
        while self.__is_running():
            try:
                self._monitor_result_queue.put_nowait(wrap_task)
                return
            except queue.Full:
                self.ev.wait(1)
                continue

    def _worker(self):
        logger.info("{name} start!".format(name=self.name))

        while self.__is_running():
            pass

        logger.info("{name} stop!".format(name=self.name))
