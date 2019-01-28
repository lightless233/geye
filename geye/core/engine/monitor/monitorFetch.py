#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.monitor.monitorFetch
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    monitor任务的监控engine
    如果通过监控用户event监控到了ID为112233的PushEvent
    那么当监控org的时候，也监控到了ID为112233的PushEvent时，应当认为是重复的
    因为我们只关心事件本身，并不关心到底是从什么途径获知该事件的

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime
import json
import queue
from typing import List, Dict

import random
import requests
from django.conf import settings
from requests import Response

from geye.core.engine.base import MultiThreadEngine
from geye.database.models import GeyeTokenModel
from geye.database.models.monitorRules import MonitorTaskTypeConstant, MonitorEventTypeConstant
from geye.utils.datatype import PriorityTask
from geye.utils.log import logger

MonitorAPIUrl = {
    MonitorTaskTypeConstant.ORG: "https://api.github.com/orgs/{org_name}/events",
    MonitorTaskTypeConstant.USER: "https://api.github.com/users/{username}/events",
    MonitorTaskTypeConstant.REPO: "https://api.github.com/repos/{owner}/{repo_name}/events",
}


class EventParser:
    """
    event的解析器
    """

    @staticmethod
    def parse_basic_item(event_data: Dict) -> Dict:
        """
        从event的内容中匹配出基础信息
        :param event_data:
        :return:
        """
        # event_id和event_type这两个字段一定存在
        event_id = event_data.get("id")
        event_type = event_data.get("type")

        # actor是一定存在的
        actor: Dict = event_data.get("actor")
        actor_url = actor.get("url")
        actor_login = actor.get("login")
        actor_display_name = actor.get("display_login")

        # repo是一定存在的
        repo: Dict = event_data.get("repo")
        repo_name = repo.get("name")
        repo_url = repo.get("url")

        # org 不一定存在，如果没有则留空
        org: Dict = event_data.get("org")
        if not org:
            org_url = ""
            org_name = ""
        else:
            org_url = org.get("url")
            org_name = org.get("login")

        # event发生的时间是一定存在的
        created_time = event_data.get("created_at")
        if created_time:
            # "created_at": "2019-01-15T09:09:13Z"，这个是UTC时间，直接转成UTC+8的时间
            strut_created_time = datetime.datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S%z")
            tz = datetime.timezone(datetime.timedelta(hours=8))
            strut_created_time = strut_created_time.astimezone(tz)
            created_time = strut_created_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "event_id": event_id,
            "event_type": event_type,
            "actor_url": actor_url,
            "actor_login": actor_login,
            "actor_display_name": actor_display_name,
            "repo_name": repo_name,
            "repo_url": repo_url,
            "org_name": org_name,
            "org_url": org_url,
            "created_time": created_time,
        }

    @staticmethod
    def parse_push_event(event_data: Dict) -> Dict:

        # 基础信息
        basic_result = EventParser.parse_basic_item(event_data)

        # payload是一定存在的
        payload: Dict = event_data.get("payload")
        payload_commits: List = payload.get("commits")
        format_payloads = []
        for _commits in payload_commits:
            author = "{username} <{email}>".format(
                username=_commits.get("author").get("name"),
                email=_commits.get("author").get("email"),
            )
            message = _commits.get("message")
            commit_url = _commits.get("url")
            format_payloads.append({
                "author": author,
                "message": message,
                "url": commit_url,
            })

        # 把解析出来的payloads放到basic_result里直接返回
        basic_result["payloads"] = format_payloads
        return basic_result

    @staticmethod
    def parse_release_event(event_data: Dict) -> Dict:
        # 基础信息
        basic_result = EventParser.parse_basic_item(event_data)

        # 解析payload
        payload: Dict = event_data.get("payload")
        release: Dict = payload.get("release")
        html_url = release.get("html_url")
        tag_name = release.get("tag_name")
        release_name = release.get("name")

        # 把解析出来的payloads放到basic_result里，直接返回
        basic_result["payloads"] = {
            "html_url": html_url,
            "tag_name": tag_name,
            "release_name": release_name
        }
        return basic_result

    @staticmethod
    def parse(event_list: list, data: str) -> Dict:
        """
        匹配event内容
        :param event_list: 待监听的事件
        :param data: 待处理的内容
        :return:
        """

        # 返回值
        retval = {
            "success": False,
            "message": "Unknown Error",
            "data": [],  # typing: List[Dict]
        }

        # json化data
        data = json.loads(data)

        # 依次处理data中的每一项
        _item: dict
        for _item in data:

            # 获取接收到的事件类型，并跳过不关心的事件
            e_type = _item.get("type", None)
            if e_type not in event_list:
                continue

            if e_type == MonitorEventTypeConstant.PUSH_EVENT:
                retval["data"].append(
                    EventParser.parse_push_event(_item)
                )
            elif e_type == MonitorEventTypeConstant.RELEASE_EVENT:
                retval["data"].append(
                    EventParser.parse_release_event(_item)
                )
            else:
                logger.error("Unknown EventType: {}".format(e_type))
                continue

        return retval


class MonitorEngine(MultiThreadEngine):

    def __init__(self, app_ctx, name, pool_size=None):
        super(MonitorEngine, self).__init__(app_ctx, name, pool_size)

        # 获取配置信息
        self.use_proxies = settings.USE_SEARCH_PROXY
        self.all_proxies = settings.SEARCH_PROXIES if self.use_proxies else []

        # 获取队列信息
        self._monitor_task_queue = self.app_ctx.MessageQueues.MONITOR_TASK_QUEUE
        self._monitor_result_queue = None

    def __is_running(self):
        # 返回当前engine是否在运行中
        # :return: True-运行状态，False-停止状态
        return self.status == self.EngineStatus.RUNNING

    def __get_task(self):
        """
        从队列中获取任务
        :return:
        """
        while self.__is_running():
            # logger.debug("queue size: {}".format(self._monitor_task_queue.qsize()))
            try:
                task: PriorityTask = self._monitor_task_queue.get_nowait()
                return task.priority, task.data
            except queue.Empty:
                self.ev.wait(1)
                continue
        else:
            return None, None

    def __put_task(self, priority, task):
        """
        放置任务到队列中
        :param priority:
        :param task:
        :return:
        """
        wrap_task = PriorityTask(priority, task)
        while self.__is_running():
            try:
                self._monitor_result_queue.put_nowait(wrap_task)
                return
            except queue.Full:
                self.ev.wait(1)
                continue

    def __wait(self, timeout: float):
        self.ev.wait(timeout)

    def __fetch_api(self, url: str) -> dict:
        """
        请求API并获取返回信息
        :param url: 待请求的API
        :return: dict
        """
        return_val = {
            "success": False,
            "reason": "unknown reason",
            "data": None
        }

        # 从db中随机读取一个token
        rows: GeyeTokenModel = GeyeTokenModel.objects.filter(is_deleted=0, status=1).all()
        if not rows:
            return_val["reason"] = "从数据库中读取token失败"
            return return_val
        row = random.choice(rows)

        # 构建请求头
        headers = {
            "Authorization": "token {}".format(row.token),
            "Accept": "application/vnd.github.v3.text-match+json",
        }

        # 获取代理信息
        proxies = random.choice(self.all_proxies) if self.use_proxies else None

        # 5次请求机会
        request_limit_cnt = 5
        while self.__is_running():
            try:
                response: Response = requests.get(url, headers=headers, timeout=12, proxies=proxies)
                status_code = response.status_code
                if status_code == 401:
                    # token有误，不要再请求了，直接返回
                    return_val["reason"] = "Token有误!"
                    return return_val
                elif status_code == 403:
                    # 触发了频率限制，等待60秒后再请求
                    request_limit_cnt -= 1
                    if not request_limit_cnt:
                        return_val["reason"] = "尝试多次请求失败，频率限制!"
                        return return_val
                    logger.error("403-Token达到请求限制, 60s后重试.")
                    self.__wait(60)
                    continue
                elif status_code == 200:
                    # 请求成功
                    return_val["success"] = True
                    return_val["data"] = response.text
                    return return_val
                else:
                    logger.error("未知错误! response: {resp}, status_code: {sc}".format(resp=response.text, sc=status_code))
                    return_val["reason"] = "请求时发生未知错误!"
                    return return_val
            except requests.RequestException as e:
                return_val["reason"] = "{e}".format(e=e)
                return return_val

    def _worker(self):
        logger.info("{name} start!".format(name=self.name))

        while self.__is_running():
            task_priority, task = self.__get_task()
            if task_priority is None or task is None:
                self.__wait(1)
                continue

            # 解析task中的数据
            # {
            #     "task_type": _row.task_type, # 可选值来自 MonitorTaskTypeConstant，监控的维度
            #     "event_type": _row.event_type, # 可选值来自MonitorEventTypeConstant，监控的事件类型，多个值用逗号分隔
            #     "rule_content": _row.rule_content, # 根据task_type有不同含义
            # }
            logger.debug("get task: {}".format(task))
            task_type = task.get("task_type", None)
            event_type: str = task.get("event_type", None)
            rule_content = task.get("rule_content", None)
            if not task_type or not event_type or not rule_content:
                self.__wait(1)
                continue

            # 根据task_type 获取不同的API接口
            api_url = MonitorAPIUrl.get(task_type, None)
            if not api_url:
                logger.error("task_type有误，无法获取API!")
                continue
            api_url = api_url.format(**json.loads(rule_content))

            # 请求API获取数据
            results = self.__fetch_api(api_url)
            if not results["success"]:
                logger.error("Fetch API failed! {err}".format(err=results["reason"]))
                continue

            logger.debug("results: {}".format(results))

            # 从API的返回中parse对应的时间内容，event_type可以为多个事件，返回格式如下
            # ret_val = {
            #     "success": False,
            #     "message": "Unknown Error",
            #     "data": [],  # typing: List[Dict]
            # }
            parse_result = EventParser.parse(event_type.split(","), results["data"])
            if not parse_result.get("success"):
                logger.error(parse_result.get("message"))
                continue
            else:
                # 把数据扔到队列里去，把event存起来
                self.__put_task(task_priority, parse_result.get("data"))

        logger.info("{name} stop!".format(name=self.name))
