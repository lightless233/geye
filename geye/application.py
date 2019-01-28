#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.application
    ~~~~~~~~~~~~~~~~

    全局的Application类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue
import signal
from typing import Union, Optional, List

from django.conf import settings

from geye.core.engine import RefreshEngine, SearchEngine, FilterEngine, SaveEngine
from geye.core.engine.monitor import MonitorRefreshEngine, MonitorEngine
from geye.utils.log import logger


class GeyeApplication(object):
    class Engines:
        """存储所有的Engines"""
        REFRESH_ENGINE: RefreshEngine = None
        SEARCH_ENGINE: SearchEngine = None
        FILTER_ENGINE: FilterEngine = None
        SAVE_ENGINE: SaveEngine = None
        MONITOR_REFRESH_ENGINE: MonitorRefreshEngine = None
        MONITOR_ENGINE: MonitorEngine = None

    class MessageQueues:
        """存储所有的消息队列"""
        # 存储搜索任务的队列
        SEARCH_TASK_QUEUE: queue.PriorityQueue = None

        # 存储过滤任务的队列
        FILTER_TASK_QUEUE: queue.PriorityQueue = None

        # 存储所有的持久化任务
        SAVE_TASK_QUEUE: queue.PriorityQueue = None

        # 存储MonitorTask的queue
        MONITOR_TASK_QUEUE: queue.PriorityQueue = None
        MONITOR_SAVE_QUEUE: queue.PriorityQueue = None

    def __init__(self, run_mode):
        super(GeyeApplication, self).__init__()
        # run_mode 有两种，分别是server 和 agent
        self.run_mode = run_mode

    def __sigint_signal_handler(self, sig, frame):
        """处理 CTRL+C 信号"""
        logger.info("Receive exit signal.")

        self.Engines.REFRESH_ENGINE.stop()
        self.Engines.SEARCH_ENGINE.stop()
        self.Engines.FILTER_ENGINE.stop()
        self.Engines.SAVE_ENGINE.stop()
        self.Engines.MONITOR_REFRESH_ENGINE.stop()
        self.Engines.MONITOR_ENGINE.stop()

    def __init_queues(self, queues: Optional[List[str]]):
        """初始化程序运行所需的队列"""
        search_queue_size = settings.SEARCH_TASK_QUEUE_SIZE or 1024
        filter_queue_size = settings.FILTER_TASK_QUEUE_SIZE or 1024
        save_queue_size = settings.SAVE_TASK_QUEUE_SIZE or 1024
        monitor_queue_size = settings.MONITOR_TASK_QUEUE_SIZE or 1024
        monitor_save_queue_size = settings.MONITOR_SAVE_QUEUE_SIZE or 1024

        if queues is None:
            # 启动所有队列
            self.MessageQueues.SEARCH_TASK_QUEUE = queue.PriorityQueue(maxsize=search_queue_size)
            self.MessageQueues.FILTER_TASK_QUEUE = queue.PriorityQueue(maxsize=filter_queue_size)
            self.MessageQueues.SAVE_TASK_QUEUE = queue.PriorityQueue(maxsize=save_queue_size)
            self.MessageQueues.MONITOR_TASK_QUEUE = queue.PriorityQueue(maxsize=monitor_queue_size)
        else:
            # 启动指定的队列
            if "search_task_queue" in queues:
                self.MessageQueues.SEARCH_TASK_QUEUE = queue.PriorityQueue(maxsize=search_queue_size)
            if "filter_task_queue" in queues:
                self.MessageQueues.FILTER_TASK_QUEUE = queue.PriorityQueue(maxsize=filter_queue_size)
            if "save_task_queue" in queues:
                self.MessageQueues.SAVE_TASK_QUEUE = queue.PriorityQueue(maxsize=save_queue_size)
            if "monitor_task_queue" in queues:
                self.MessageQueues.MONITOR_TASK_QUEUE = queue.PriorityQueue(maxsize=monitor_queue_size)
            if "monitor_save_queue" in queues:
                self.MessageQueues.MONITOR_SAVE_QUEUE = queue.PriorityQueue(maxsize=monitor_save_queue_size)

    def __init_engines(self, engines: Optional[List[str]]):
        """初始化所需的engine"""
        if engines is None:
            self.Engines.SAVE_ENGINE = SaveEngine(app_ctx=self, name="SaveEngine")
            self.Engines.SAVE_ENGINE.start()

            self.Engines.FILTER_ENGINE = FilterEngine(app_ctx=self, name="FilterEngine")
            self.Engines.FILTER_ENGINE.start()

            self.Engines.SEARCH_ENGINE = SearchEngine(app_ctx=self, name="SearchEngine")
            self.Engines.SEARCH_ENGINE.start()

            self.Engines.REFRESH_ENGINE = RefreshEngine(app_ctx=self, name="RefreshEngine")
            self.Engines.REFRESH_ENGINE.start()

            self.Engines.MONITOR_ENGINE = MonitorEngine(app_ctx=self, name="MonitorEngine")
            self.Engines.MONITOR_ENGINE.start()

            self.Engines.MONITOR_REFRESH_ENGINE = MonitorRefreshEngine(app_ctx=self, name="MonitorRefreshEngine")
            self.Engines.MONITOR_REFRESH_ENGINE.start()
        else:
            if "save_engine" in engines:
                self.Engines.SAVE_ENGINE = SaveEngine(app_ctx=self, name="SaveEngine")
                self.Engines.SAVE_ENGINE.start()
            if "filter_engine" in engines:
                self.Engines.FILTER_ENGINE = FilterEngine(app_ctx=self, name="FilterEngine")
                self.Engines.FILTER_ENGINE.start()
            if "search_engine" in engines:
                self.Engines.SEARCH_ENGINE = SearchEngine(app_ctx=self, name="SearchEngine")
                self.Engines.SEARCH_ENGINE.start()
            if "refresh_engine" in engines:
                self.Engines.REFRESH_ENGINE = RefreshEngine(app_ctx=self, name="RefreshEngine")
                self.Engines.REFRESH_ENGINE.start()
            if "monitor_refresh_engine" in engines:
                self.Engines.MONITOR_REFRESH_ENGINE = MonitorRefreshEngine(app_ctx=self, name="MonitorRefreshEngine")
                self.Engines.MONITOR_REFRESH_ENGINE.start()
            if "monitor_engine" in engines:
                self.Engines.MONITOR_ENGINE = MonitorEngine(app_ctx=self, name="MonitorEngine")
                self.Engines.MONITOR_ENGINE.start()

    def start(self, queues=None, engines=None):

        # 注册CTRL+C处理器
        signal.signal(signal.SIGINT, self.__sigint_signal_handler)

        run_mode = self.run_mode
        if run_mode == "server":
            # 以server模式启动，仅启动refresh engine和save engine
            pass
        elif run_mode == "agent":
            # 以agent模式启动，仅启动search engine和filter engine
            pass
        elif run_mode == "single":
            # 单机模式启动，启动自己的队列和全部engine
            self.__init_queues(queues=None)
            self.__init_engines(engines=None)
        elif run_mode == "test":
            self.__init_queues(queues=queues)
            self.__init_engines(engines=engines)
        else:
            raise RuntimeError("错误的启动参数! 不支持: {}".format(run_mode))
