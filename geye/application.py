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


class GeyeApplication(object):
    class Engines:
        """存储所有的Engines"""
        REFRESH_ENGINE = None

    class MessageQueues:
        """存储所有的消息队列"""
        # 存储搜索任务的队列
        SEARCH_TASK_QUEUE: queue.PriorityQueue = None

        # 存储过滤任务的队列
        FILTER_TASK_QUEUE: queue.PriorityQueue = None

    def __init__(self, run_mode):
        super(GeyeApplication, self).__init__()
        self.run_mode = run_mode

    def __start_queues(self):
        self.MessageQueues.SEARCH_TASK_QUEUE = queue.PriorityQueue(maxsize=1024)

    def start(self):
        self.__start_queues()
