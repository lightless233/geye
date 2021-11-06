#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    save.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import queue

from geye.core.engine.base import SingleThreadEngine
from geye.database.models.yuque.leaks import GeyeYuqueLeaksModel
from geye.utils.log import logger


class YuqueSaveEngine(SingleThreadEngine):

    def __init__(self, app_ctx, name):
        super(YuqueSaveEngine, self).__init__(app_ctx, name)

        self.save_queue = self.app_ctx.MessageQueues.YUQUE_SAVE_QUEUE

    def _get_task(self):
        while self.is_running():
            try:
                _task = self.save_queue.get_nowait()
                return _task.priority, _task.data
            except queue.Empty:
                self.ev.wait(1)
                continue

    def _worker(self):
        logger.debug("{} start.".format(self.name))
        while self.is_running():
            _, task = self._get_task()
            if not task:
                continue

            rule_id = task.get("rule_id")
            result_list = task.get("results")

            for result in result_list:
                leak = GeyeYuqueLeaksModel()
                leak.title = result.get("title")
                leak.go_url = result.get("url")
                leak.url = result.get("raw_url")
                leak.book_name = result.get("book_name")
                leak.group_name = result.get("group_name")
                leak.abstract = result.get("abstract")
                leak.search_rule_obj = result.get("")
                leak.search_rule_id = rule_id
                leak.status = 1
                leak.content_updated_at = task.get("content_updated_at")
                leak.first_published_at = task.get("first_published_at")
                leak.paper_created_at = task.get("created_at")
                leak.paper_updated_at = task.get("updated_at")
                leak.save()
                logger.debug("Save yuque leak <<{}>>".format(result.get("title")))

        logger.debug("{} end.".format(self.name))
