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
import json
import queue

from geye.core.engine.base import SingleThreadEngine
from geye.database.models import GeyeMonitorResultsModel
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
            # 从队列中获取任务
            task_priority, task = self.__get_task_from_queue()
            if not task_priority or not task:
                continue

            # 任务格式
            # {
            #   "data": [{}..],
            #   "monitor_rule_id": int,
            # }
            # data中的每一项结构如下
            # {
            #     "event_id": event_id,
            #     "event_type": event_type,
            #     "actor_url": actor_url,
            #     "actor_login": actor_login,
            #     "actor_display_name": actor_display_name,
            #     "repo_name": repo_name,
            #     "repo_url": repo_url,
            #     "org_name": org_name,
            #     "org_url": org_url,
            #     "created_time": created_time,
            #     "payloads": {}
            # }

            monitor_rule_id = task.get("monitor_rule_id")
            if not monitor_rule_id:
                continue

            dataset = task.get("data")
            for item in dataset:
                monitor_results = GeyeMonitorResultsModel()
                monitor_results.monitor_rule_id = monitor_rule_id
                monitor_results.event_id = item.get("event_id")
                monitor_results.event_type = item.get("event_type")

                monitor_results.actor_url = item.get("actor_url")
                monitor_results.actor_login = item.get("actor_login")
                monitor_results.actor_display_name = item.get("actor_display_name")

                monitor_results.org_name = item.get("org_name")
                monitor_results.org_url = item.get("org_url")

                monitor_results.repo_url = item.get("repo_url")
                monitor_results.repo_name = item.get("repo_name")

                monitor_results.event_created_time = item.get("created_time")

                monitor_results.content = json.dumps(item.get("payloads") or {})

                monitor_results.save()

        logger.info("{name} stop!".format(name=self.name))

