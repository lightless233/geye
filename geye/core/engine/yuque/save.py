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
        self._real_worker()
        logger.debug("{} end.".format(self.name))

    def _real_worker(self):
        pass
