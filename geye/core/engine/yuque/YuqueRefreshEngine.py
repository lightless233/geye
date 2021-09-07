#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    YuqueRefreshEngine
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import datetime
import queue
from typing import Iterable

from geye.core.engine.base import SingleThreadEngine
from geye.database.models.yuque.rules import GeyeYuqueSearchRuleModel
from geye.utils.datatype import PriorityTask
from geye.utils.logger import LoggerFactory


class YuqueRefreshEngine(SingleThreadEngine):
    """
    定时产生语雀的监控任务
    """

    logger = LoggerFactory.get_logger(__name__)

    def __init__(self, app_ctx, name="YuqueRefresh"):
        super(YuqueRefreshEngine, self).__init__(app_ctx, name)

        self._task_queue = self.app_ctx.MessageQueues.YUQUE_TASK_QUEUE

    def _worker(self):
        self.logger.info(f"{self.name} start!")

        while self.is_running():
            self.logger.debug("start build yuque search task.")

            rows: Iterable[GeyeYuqueSearchRuleModel] = GeyeYuqueSearchRuleModel.instance.all_enable_rules()
            for row in rows:
                interval = row.interval
                last_refresh_time = row.last_refresh_time

                # 判断是否存在需要生成任务的关键字
                if last_refresh_time + datetime.timedelta(minutes=interval) > datetime.datetime.now():
                    continue

                # 生成搜索任务
                task = PriorityTask(row.priority, {
                    "rule_id": row.id,
                    "rule_content": row.rule,
                })

                self.logger.debug(f"Create yuque search task: {task}")

                # 添加到任务队列
                while self.is_running():
                    try:
                        self._task_queue.put_nowait(task)
                        break
                    except queue.Full:
                        self.ev.wait(3)
                        continue

            self.ev.wait(30)

        self.logger.info(f"{self.name} stop!")
