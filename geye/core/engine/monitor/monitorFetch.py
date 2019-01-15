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
    def parse_push_event(event_data: dict) -> dict:
        # event_id和event_type这两个字段一定存在
        event_id = event_data.get("id")
        event_type = event_data.get("type")

        # actor应该也是一定存在的
        actor: Dict = event_data.get("actor")
        actor_url = actor.get("url")
        actor_login = actor.get("login")
        actor_display_name = actor.get("display_login")

        # org 不一定存在

        # 基础信息也是一定存在的
        created_time = event_data.get("created_at")


    @staticmethod
    def parse_release_event(event_data: dict) -> dict:
        pass

    @staticmethod
    def parse(event_list: list, data: str) -> dict:
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
            "data": [],     # typing: List[Dict]
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

            # 从API的返回中parse对应的时间内容，event_type可以为多个事件
            parse_result = EventParser.parse(event_type.split(","), results["data"])

            # 把event存起来
            # self.__save_events(events)

        logger.info("{name} stop!".format(name=self.name))
