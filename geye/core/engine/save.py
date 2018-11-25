#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.save
    ~~~~~~~~~~~~~~~~~~~~~

    将任务存储的PostgreSQL中
    如果太慢了，考虑改成线程池

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue

from django.db import Error as DBError

from geye.database.models import GeyeLeaksModel
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger
from .base import SingleThreadEngine


class SaveEngine(SingleThreadEngine):
    def __init__(self, app_ctx, name):
        super(SaveEngine, self).__init__(app_ctx, name)

        # 获取队列信息
        self.save_queue = self.app_ctx.MessageQueues.SAVE_TASK_QUEUE

    def get_task_from_queue(self):
        while self.status == self.EngineStatus.RUNNING:
            try:
                task: PriorityTask = self.save_queue.get_nowait()
                return task.priority, task.data
            except queue.Empty:
                self.ev.wait(1)
                continue
        else:
            return None, None

    def _worker(self):
        logger.info("{} start!".format(self.name))

        while self.status == self.EngineStatus.RUNNING:
            task_priority, task = self.get_task_from_queue()
            if not task_priority or not task:
                continue

            filter_task = task["filter_task"]

            if GeyeLeaksModel.instance.is_exist(filter_task["sha"]):
                # 已经有这条记录了，continue
                continue

            # 存储数据
            try:
                GeyeLeaksModel.objects.create(
                    repo_name=filter_task["repo_name"],
                    author=filter_task["author"],
                    path=filter_task["path"],
                    filename=filter_task["filename"],
                    sha=filter_task["sha"],
                    full_code_url=filter_task["full_code_url"],
                    url=filter_task["url"],
                    code=task["code"],
                    srid=filter_task["srid"],
                    frid=task["frid"],
                    status=task["status"],
                    pushed=task["pushed"],
                )
            except DBError as e:
                logger.error("SaveEngine error: {}".format(e))
                # todo: send error message
                continue

            # post-action
            # todo: send notification
            # todo: clone repo

        logger.info("{} end!".format(self.name))
