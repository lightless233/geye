#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.search
    ~~~~~~~~~~~~~~~~~~~~~~~

    使用search rule在github上进行第一次初步搜索
    todo: 改成协程

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import gzip
import json
import queue
import random
import threading
from typing import Optional

import requests
from django.conf import settings

from geye.database.models import GeyeTokenModel
from .base import MultiThreadEngine
from geye.utils.log import logger


class SearchEngine(MultiThreadEngine):
    def __init__(self, app_ctx, name, pool_size=None):
        super(SearchEngine, self).__init__(app_ctx, name, pool_size)

        # 获取配置信息
        self.search_api_url = settings.GITHUB_API_SEARCH_URL
        self.search_page_max_size = settings.SEARCH_PAGE_SIZE
        self.each_page_item_size = settings.EACH_PAGE_ITEM_SIZE

        # 获取代理信息
        self.use_proxies = settings.USE_SEARCH_PROXY
        self.all_proxies = settings.SEARCH_PROXIES if self.use_proxies else []

        # 获取队列信息
        self.search_task_queue: queue.PriorityQueue = self.app_ctx.MessageQueues.SEARCH_TASK_QUEUE
        self.filter_task_queue: queue.PriorityQueue = self.app_ctx.MessageQueues.FILTER_TASK_QUEUE

    def alive_count(self):
        """获取当前存活的线程数量"""
        return sum([t.is_alive() for t in self.thread_pool])

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

    @staticmethod
    def build_request_header() -> Optional[dict]:
        """
        OAuth2 Token (sent in a header)
            curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com
        从数据库中获取一个剩余次数最大的token
        """
        token = GeyeTokenModel.objects.filter(is_deleted=0, status=1).order_by("-remain_limit").first()
        if not token:
            return None
        else:
            return {
                "Authorization": "token {}".format(token),
                "Accept": "application/vnd.github.v3.text-match+json",
            }

    def build_request_data(self, rule_content, page_num) -> dict:
        return {
            "q": "{}+fork:false".format(rule_content),
            "sort": "indexed",
            "per_page": self.each_page_item_size,
            "page": page_num if page_num else 1
        }

    def make_request(self, header, data) -> requests.Response:
        """
        发出搜索请求
        :param header: 请求的header，包括token等信息
        :param data: 搜索的内容
        todo: 增加失败次数，防止一直都进行重复请求
        """

        # 获取代理设置信息
        proxies = random.choice(self.all_proxies) if self.use_proxies else None

        while True:
            try:
                response = requests.get(
                    self.search_api_url, params=data, headers=header, timeout=12, proxies=proxies
                )
                return response
            except requests.RequestException as e:
                logger.error("Error while make request. requests.RequestException: {}".format(e))
                logger.error("Try re-request after 5s.")
                self.ev.wait(5)
                continue

    def parse_response(self, response: requests.Response, srid, rule_name) -> dict:
        """
        解析response对象的结果，解析出所有的代码数据
        :return:
            {
                # 所有拿到的代码信息
                "filter_tasks": [
                    {filter_task-1}
                    {filter_task-2}
                    ...
                ],
                # 如果当前response没有数据，则将该字段设置为False
                # 表示不再继续请求下一页，节省token limit
                # 如果当前数据数量与配置中的每页数量不符，也认为没有下一页了
                # 同时将该字段设置为False
                # True-应当继续请求下一页
                # False-没有下一页了，停止请求
                "has_next_page": True/False
                # 错误信息，如果没错误，则设置为None
                "error": None/"error message"
            }
        """
        return_val = {
            "filter_tasks": [],
            "has_next_page": True,
            "error": None
        }
        raw_content = response.text

        # 尝试解析JSON内容
        try:
            result = json.loads(raw_content)
        except UnicodeDecodeError:
            _decode_result = gzip.decompress(raw_content)
            try:
                result = json.loads(_decode_result)
            except json.JSONDecodeError:
                logger.error("Receive invalid content, JSON decode fail. content: {}".format(raw_content))
                return_val["error"] = "JSON decode fail."
                return return_val

        # 从JSON对象中获取信息
        items = result.get("items")
        if not items:
            # 当前response对象无数据，直接返回，无需请求下一页
            return_val["has_next_page"] = False
            return return_val
        if len(items) < self.each_page_item_size:
            # 当前response对象的数据小于设置的每页数量，解析后返回，无需请求下一页
            return_val["has_next_page"] = False

        for _item in items:
            # _item的格式参照: https://developer.github.com/v3/search/#example-2
            repo_info = _item.get("repository")
            author = repo_info.get("owner").get("login")
            repo_name = repo_info.get("name")
            filename = _item.get("name")
            path = _item.get("path")
            sha = _item.get("sha")
            url = _item.get("html_url")
            full_code_url = url.replace("https://github.com", "https://raw.githubusercontent.com")
            full_code_url = full_code_url.replace("blob/", "")

            # 组装filter task
            filter_task = {
                "author": author,
                "repo_name": repo_name,
                "filename": filename,
                "path": path,
                "sha": sha,
                "url": url,
                "full_code_url": full_code_url,
                "srid": srid,
                "search_rule_name": rule_name,
            }
            return_val["filter_tasks"].append(filter_task)
        return return_val

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
            for page_num in range(1, self.search_page_max_size + 1):
                request_data = self.build_request_data(rule_content, page_num)
                request_header = self.build_request_header()
                if request_header is None:
                    logger.error("No available token found. Jumping search operator.")
                    break

                logger.debug("Fetch data: {}, header: {}".format(request_data, request_header))

                # 发起请求
                response: requests.Response = self.make_request(request_header, request_data)
                while response.status_code != 200:
                    # 触发了频率限制，等60s重新请求当前page
                    # todo: 换个token请求
                    # todo: 增加错误次数限制，防止无限制请求
                    logger.error("Trigger GITHUB abusing limit. Try re-request after 60s. "
                                 "request data: {}, request header: {}".format(request_data, request_header))
                    self.ev.wait(60)
                    logger.debug("After 60s, try re-request to bypass abusing limit.")
                    response: requests.Response = self.make_request(request_header, request_data)

                # 正常内容 开始解析内容
                # return_val = {
                #     "filter_tasks": [],
                #     "has_next_page": True,
                #     "error": None
                # }
                results = self.parse_response(response, srid, rule_name)
                if results["error"]:
                    # 解析有问题，这里是否需要重新请求当前页？
                    continue

                # 将生成的filter_task放入filter队列
                for task in results["filter_tasks"]:
                    self.push_to_queue(task_priority, task)

                # 根据has_next_page字段决定是否请求下一页
                if not results["has_next_page"]:
                    logger.debug("Jump remains page because of 'has_next_page' is False.")
                    break

        logger.info("{} end!".format(current_name))
