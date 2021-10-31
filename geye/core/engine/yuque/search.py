#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.engine.yuque.search
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    调用语雀的 HTTP 接口获取数据

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import logging
import queue
import random
import threading

import requests
from django.conf import settings

from geye.database.models import GeyeCookieModel
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger
from ..base import MultiThreadEngine


class YuqueSearchEngine(MultiThreadEngine):
    """
    语雀信息搜索
    TODO：后面把一些写死的参数移动到配置文件里
    """

    SEARCH_API = "https://www.yuque.com/api/zsearch"

    def __init__(self, app_ctx, name, pool_size=None):
        super(YuqueSearchEngine, self).__init__(app_ctx, name, pool_size)

        # 获取代理信息
        self._use_proxy = settings.USE_SEARCH_PROXY
        self._proxies = settings.SEARCH_PROXIES if self._use_proxy else []

        # 队列相关的信息
        self.search_queue = self.app_ctx.MessageQueues.YUQUE_TASK_QUEUE
        self.save_queue = self.app_ctx.MessageQueues.YUQUE_SAVE_QUEUE

    @staticmethod
    def __encode_keyword(keyword) -> str:
        """
        对搜索词进行 Unicode 编码，绕过语雀的黑名单检查
        :param keyword:
        :return:
        """
        keyword_list = keyword.split(" ")
        escaped_keyword_list = list(map(lambda x: x.encode("unicode_escape").decode("utf8"), keyword_list))
        return "+".join(escaped_keyword_list)

    def _get_task(self):
        """
        从队列中获取一个搜索任务
        :return:
        """
        while self.is_running():
            try:
                task = self.search_queue.get_nowait()
                return task.priority, task.data
            except queue.Empty:
                self.ev.wait(1)
                continue
        else:
            return None, None

    def _put_task(self, task):
        """
        把结果塞到队列中
        :return:
        """
        while self.is_running():
            try:
                self.save_queue.put_nowait(task)
                break
            except queue.Full:
                self.ev.wait(1)
                continue

    def make_request(self, url, header, data):
        """
        发起 HTTP 请求，对于语雀的请求，需要加载一个有效的 cookie
        如果请求出现问题，会重试3次
        TODO：重试的相关配置，放到配置文件中
        :param url:
        :param header:
        :param data:
        :return:
        """

        req_cnt = 0
        max_retry = 3
        while self.is_running():
            try:
                req_cnt += 1
                if req_cnt >= max_retry:
                    logger.error("max retry exceeded")
                    break

                # 如果设置了需要使用代理，随机选取一个代理配置
                if self._use_proxy:
                    proxies = random.choice(self._proxies)
                else:
                    proxies = None
                response = requests.get(url, params=data, headers=header, timeout=9, proxies=proxies)
                return response
            except requests.RequestException as e:
                logger.error("Error while make request to {}. Error: {}. retry in 3 seconds...".format(url, e))
                self.ev.wait(3)
                continue

        return None

    @staticmethod
    def _get_cookie_header() -> str:
        yuque_cookie_list = GeyeCookieModel.instance.get_by_domain("yuque.com")
        cookie_value_list = []
        for _cookie in yuque_cookie_list:
            value = _cookie.value
            cookie_value_list.append(value if value.endswith(";") else value + ";")

        return " ".join(cookie_value_list)

    @staticmethod
    def parse_response(response):
        """
        解析 yuque 接口返回的 response
        :param response:
        :return:
        """
        result = response.json()
        data = result.get("data")
        total_hits = data.get("totalHits")
        num_hits = data.get("numHits")

        # 打个log看看
        logger.debug("total_hits: {}, num_hits".format(total_hits, num_hits))

        # 这里面是命中的信息
        hits_list = data.get("hits")

        ret_list = []
        for hits in hits_list:
            abstract = hits.get("abstract", "NO_ABSTRACT_FIELD")
            book_name = hits.get("book_name", "NO_BOOK_NAME_FIELD")
            group_name = hits.get("group_name", "NO_GROUP_NAME_FIELD")
            paper_id = hits.get("id", "NO_ID_FIELD")
            url = hits.get("url", "NO_URL_FIELD")
            title = hits.get("title", "NO_TITLE_FIELD")

            record = hits.get("record", None)
            if record:
                content_updated_at = record.get("content_updated_at", "")
                first_published_at = record.get("first_published_at", "")
                published_at = record.get("published_at", "")
                created_at = record.get("created_at", "")
                updated_at = record.get("updated_at", "")
            else:
                content_updated_at = ""
                first_published_at = ""
                published_at = ""
                created_at = ""
                updated_at = ""

            # 如果开启了获取真实链接的配置，那么再请求一次获取真实的文章URL
            # TODO 现在默认获取，以后把这个配置项移动到配置文件里
            paper_full_url = "https://yuque.com{}".format(url)
            redirect_path = requests.get(paper_full_url, timeout=9).history[-1].headers.get("location")
            paper_raw_url = "https://yuque.com{}".format(redirect_path)

            ret_list.append({
                "abstract": abstract,
                "book_name": book_name,
                "group_name": group_name,
                "id": paper_id,
                "title": title,
                "url": url,
                "raw_url": paper_raw_url,
                "content_updated_at": content_updated_at,
                "first_published_at": first_published_at,
                "published_at": published_at,
                "created_at": created_at,
                "updated_at": updated_at,
            })
        return ret_list

    def _worker(self):
        c_name = threading.current_thread().name
        logger.info("{} start!".format(c_name))
        self._real_worker()
        logging.info("{} stop.".format(c_name))

    def _real_worker(self):
        while self.is_running():
            priority, task = self._get_task()
            if not priority or not task:
                continue

            # 解析任务内容
            # "rule_id": row.id,
            # "rule_content": row.rule,
            rule_content = task.get("rule_content")
            if not rule_content:
                continue

            # 构建请求的参数
            # 有几个参数是必须的
            # p 是页码，q是搜索词
            params = {
                "tab": "public",
                "scope": "/",
                "type": "content",
                "q": self.__encode_keyword(rule_content)
            }

            # 默认搜索 3 页
            results = []
            for p in range(1, 4):
                params["p"] = p
                # 从 db 里取出 yuque.com 域名的 cookie 信息
                # 先写死 "yuque.com"

                header = {
                    "Cookie": self._get_cookie_header()
                }
                logger.debug("yuque header: {}".format(header))
                response = self.make_request(self.SEARCH_API, header, params)
                parsed_result = self.parse_response(response)
                results.extend(parsed_result)

            # 放进队列中
            self._put_task(PriorityTask(priority, results))
