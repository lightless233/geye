#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.refresh
    ~~~~~~~~~~~~~~~~~~~~~~~~

    定时产生需要监控的任务

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime
import queue
import time

from django.conf import settings

from .base import SingleThreadEngine
from geye.utils.log import logger
from geye.database.models import GeyeSearchRuleModel
from geye.utils.datatype import PriorityTask


class RefreshEngine(SingleThreadEngine):

    def __init__(self, app_ctx, name=None):
        super(RefreshEngine, self).__init__(app_ctx, name)

    def _worker(self):

        logger.info("RefreshEngine start!")

        refresh_task_queue = self.app_ctx.MessageQueues.SEARCH_TASK_QUEUE

        while self.status == self.EngineStatus.RUNNING:
            logger.debug("start build search task.")
            rows = GeyeSearchRuleModel.objects.filter(is_deleted=0, status=1).all()
            current_time = datetime.datetime.now()

            for row in rows:
                delay = int(row.delay)
                if row.last_refresh_time + datetime.timedelta(minutes=delay) < current_time:
                    # 该刷新了，添加到任务队列中去
                    # 添加一个字典，如果后续改成分布式，需要改成JSON字符串
                    # Task格式：
                    #   tuple(priority, _task)

                    # build task
                    _data = {
                        "search_rule_id": row.id,
                        "search_rule_name": row.name,
                        "search_rule_content": row.rule,
                    }
                    # task = (row.priority, _data)
                    task = PriorityTask(row.priority, _data)
                    logger.debug("task: {}".format(task))
                    while True:
                        try:
                            refresh_task_queue.put_nowait(task)
                            break
                        except queue.Full:
                            self.ev.wait(3)
                            continue

                    # 更新任务的最后刷新时间
                    row.last_refresh_time = current_time
                    row.save()

            self.ev.wait(settings.REFRESH_INTERVAL)

        logger.info("RefreshEngine end!")
