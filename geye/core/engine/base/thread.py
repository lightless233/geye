#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.base.thread
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    基于线程的engine基类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import threading
import abc
import typing

from .base import CommonBaseEngine

if typing.TYPE_CHECKING:
    from geye.application import GeyeApplication


class SingleThreadEngine(CommonBaseEngine):
    def __init__(self, app_ctx: GeyeApplication, name=None):
        super(SingleThreadEngine, self).__init__()
        self.name = name if name else "SingleThreadEngine"
        self.app_ctx: GeyeApplication = app_ctx

    def start(self):
        self.thread: threading.Thread = threading.Thread(target=self._worker, name=self.name)
        self.thread.start()
        self.status = self.EngineStatus.RUNNING

    def stop(self, force=True):
        self.status = self.EngineStatus.STOP
        self.ev.set()

    def is_alive(self):
        return self.thread.is_alive()

    @abc.abstractmethod
    def _worker(self):
        pass
