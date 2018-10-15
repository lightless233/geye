#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.search
    ~~~~~~~~~~~~~~~~~~~~~~~

    使用search rule在github上进行第一次初步搜索

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue
import threading

import requests
from django.conf import settings

from .base import MultiThreadEngine
from geye.utils.log import logger


class SearchEngine(MultiThreadEngine):
    def __init__(self, app_ctx, name=None, pool_size=None):
        super(SearchEngine, self).__init__(app_ctx, name, pool_size)
        self.search_api_url = settings.GITHUB_API_SEARCH_URL
        self.search_page_max_size = settings.SEARCH_PAGE_SIZE

        self.search_task_queue: queue.PriorityQueue = self.app_ctx.MessageQueues.SEARCH_TASK_QUEUE
        self.filter_task_queue: queue.PriorityQueue = self.app_ctx.MessageQueues.FILTER_TASK_QUEUE

    def alive_count(self):
        """获取当前存活的线程数量"""
        return sum([t.is_alive() for t in self.thread_pool])

    def build_request_header(self):
        pass

    def build_request_data(self):
        pass

    def get_task_from_queue(self):
        """
        从队列中获取任务，并且解析出真正的内容
        :return: tuple (优先级, 任务数据dict)
        """
        while True:
            try:
                task = self.search_task_queue.get_nowait()
                break
            except queue.Empty:
                self.ev.wait(1)
                continue
        return task[0], task[1]

    def push_to_queue(self, priority, filter_task):
        task = (priority, filter_task)
        while True:
            try:
                self.filter_task_queue.put_nowait(task)
                break
            except queue.Full:
                self.ev.wait(1)
                continue

    def _worker(self):
        current_name = threading.current_thread().name
        logger.info("{} start!".format(current_name))

        while self.status == self.EngineStatus.RUNNING:
            # 获取任务信息
            task_priority, search_task = self.get_task_from_queue()
            srid = search_task.get("search_rule_id")
            rule_name = search_task.get("search_rule_name")
            rule_content = search_task.get("search_rule_content")

            # 循环请求每一页
            for page_num in range(1, self.search_page_max_size+1):
                request_data = self.build_request_data(rule_content, page_num)
                request_header = self.build_request_header()
                response: requests.Response = self.make_request(request_header, request_data)

                if response.status_code != 200:
                    # 触发了频率限制，等60s重新请求当前page
                    pass

                # 正常内容 开始解析内容
                filter_task = pares_response()

                # 将生成的filter_task放入filter队列
                self.push_to_queue(task_priority, filter_task)

        logger.info("{} end!".format(current_name))
