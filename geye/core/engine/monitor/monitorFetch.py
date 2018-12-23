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
import json
import queue

import random
from django.conf import settings

from geye.core.engine.base import MultiThreadEngine
from geye.database.models import GeyeTokenModel
from geye.database.models.monitorRules import MonitorTaskTypeConstant
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger


MonitorAPIUrl = {
    MonitorTaskTypeConstant.ORG: "https://api.github.com/orgs/{org_name}/events",
    MonitorTaskTypeConstant.USER: "https://api.github.com/users/{username}/events",
    MonitorTaskTypeConstant.REPO: "https://api.github.com/repos/{owner}/{repo_name}/events",
}


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
        # 返回当前engine是否在运行中
        # :return: True-运行状态，False-停止状态
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

    def __wait(self, timeout: float):
        self.ev.wait(timeout)

    def __fetch_api(self, url: str) -> dict:
        """
        请求API并获取返回信息
        :param url: 待请求的API
        :return: dict
        """
        return_val = {
            "success": False,
            "reason": "unknown reason",
            "data": None
        }

        # 从db中随机读取一个token
        rows: GeyeTokenModel = GeyeTokenModel.objects.filter(is_deleted=0, status=1).all()
        if not rows:
            return_val["reason"] = "从数据库中读取token失败"
            return return_val
        row = random.choice(rows)

        # 构建请求头
        headers = {
            "Authorization": "token {}".format(row.token),
            "Accept": "application/vnd.github.v3.text-match+json",
        }

    def _worker(self):
        logger.info("{name} start!".format(name=self.name))

        while self.__is_running():
            task_priority, task = self.__get_task()
            if task_priority is None or task is None:
                self.__wait(1)
                continue

            # 解析task中的数据
            # {
            #     "task_type": _row.task_type, # 可选值来自 MonitorTaskTypeConstant，监控的维度
            #     "event_type": _row.event_type, # 可选值来自MonitorEventTypeConstant，监控的事件类型
            #     "rule_content": _row.rule_content, # 根据task_type有不同含义
            # }
            task_type = task.get("task_type", None)
            event_type = task.get("event_type", None)
            rule_content = task.get("rule_content", None)
            if not task_type or not event_type or not rule_content:
                self.__wait(1)
                continue

            # 根据task_type 获取不同的API接口
            api_url = MonitorAPIUrl.get(task_type, None)
            if not api_url:
                logger.error("task_type有误，无法获取API!")
                continue
            api_url = api_url.format(**json.loads(rule_content))

            # 请求API获取数据
            # results = self.__fetch_api(api_url)

            # 从API的返回中parse对应的时间内容，event_type可以为多个事件
            # events = self.__parse_event(results, event_type)

            # 把event存起来
            # self.__save_events(events)

        logger.info("{name} stop!".format(name=self.name))
