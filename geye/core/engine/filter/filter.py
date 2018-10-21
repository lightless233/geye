#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.filter
    ~~~~~~~~~~~~~~~~~~~~~~~

    Filter引擎，负责过滤抓取到的代码

    从队列中获取到的task格式
    {
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

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import queue
import threading
from typing import List
import random

import requests
from django.conf import settings

from geye.core.engine.base import MultiThreadEngine
from geye.database.models import GeyeFilterRuleModel
from geye.database.models import LeaksStatusConstant
from geye.utils.log import logger
from .rule import RuleEngine


class FilterEngine(MultiThreadEngine):
    def __init__(self, app_ctx, name, pool_size=None):
        super(FilterEngine, self).__init__(app_ctx, name, pool_size)

        # 获取队列
        self.filter_task_queue = app_ctx.MessageQueues.FILTER_TASK_QUEUE
        self.save_task_queue = app_ctx.MessageQueues.SAVE_TASK_QUEUE

        # 获取代理信息
        self.use_proxies = settings.USE_SEARCH_PROXY
        self.all_proxies = settings.SEARCH_PROXIES if self.use_proxies else []

    def get_task_from_queue(self):
        """
        从队列中解析出任务信息来
        """
        while self.status == self.EngineStatus.RUNNING:
            try:
                task = self.filter_task_queue.get_nowait()
                return task
            except queue.Empty:
                self.ev.wait(1)
                continue

    @staticmethod
    def get_filter_rules(srid) -> list:
        """
        获取所有需要匹配的规则，先获取全局filter规则，再获取子filter规则
        :param srid: search rule id
        :return: list
        """
        filter_rules = GeyeFilterRuleModel.instance.get_filter_rules_by_srid(srid)
        return filter_rules

    def get_raw_code(self, raw_code_url):
        """
        获取完整的代码文件内容
        :return:
        """

        result = {
            "success": False,
            "code": ""
        }

        if self.use_proxies:
            proxies = random.choice(self.all_proxies)
        else:
            proxies = None

        # 发出请求
        try:
            response = requests.get(raw_code_url, timeout=15, proxies=proxies)
            result["code"] = response.text
            result["success"] = True
        except requests.RequestException:
            logger.error("Error while get raw code. Will re-put filter task to queue. URL: {}".format(raw_code_url))

        return result

    def put_task_to_queue(self, task, target_queue: queue.PriorityQueue = None):
        if not target_queue:
            target_queue = self.filter_task_queue
        while self.status == self.EngineStatus.RUNNING:
            try:
                target_queue.put_nowait(task)
                break
            except queue.Full:
                self.ev.wait(1)
                continue

    @staticmethod
    def __get_content_by_position(position, task, raw_code):
        position = int(position)
        result = {
            "success": True,
            "filter_content": ""
        }
        if position == 1:
            # repo author
            filter_content = task.get("author", "")
        elif position == 2:
            # repo name
            filter_content = task.get("repo_name", "")
        elif position == 3:
            # path
            filter_content = task.get("path", "")
        elif position == 4:
            # code
            filter_content = raw_code
        elif position == 5:
            # filename
            filter_content = task.get("filename", "")
        else:
            filter_content = ""
            result["success"] = False

        result["filter_content"] = filter_content
        return result

    def do_filter(self, rule: GeyeFilterRuleModel, task: dict, raw_code: str):
        """
        根据规则进行过滤
        # 1. 根据规则的position字段获取需要匹配的内容
        # 2. 根据规则类型执行不同的匹配，返回匹配结果
        # 3. 根据rule的action进行后续处理

        :param rule: 规则model
        :param task: 队列中获取到的task对象
        :param raw_code: 完整的代码
        :return:
        """
        # 返回的对象
        rv = {
            "error": False,
            "found": False,
            "code": ""
        }

        # 获取待匹配的内容
        result = self.__get_content_by_position(rule.position, task, raw_code)
        if not result["success"]:
            # 获取内容失败了，直接返回，不匹配了
            return False
        content = result["filter_content"]

        if rule.rule_engine == 1:
            # 正则匹配，使用设置里指定的正则引擎，支持grep引擎和raw引擎
            # grep引擎：调用系统的grep命令
            # raw引擎：使用Python自带的正则引擎
            filter_result = RuleEngine.regex_filter(rule.rule, content, rule.id)
            rv["error"] = filter_result["error"]
            rv["found"] = filter_result["found"]
            rv["code"] = filter_result["code"]
            return rv
        elif rule.rule_engine == 2:
            # 字符串匹配
            filter_result = RuleEngine.string_filter(rule.rule, content)
            rv["error"] = filter_result["error"]
            rv["found"] = filter_result["found"]
            rv["code"] = filter_result["code"]
            return rv
        else:
            logger.error("unknown filter engine, rule_engine: '{}'".format(rule.rule_engine))
            return False

    def _worker(self):
        current_name = threading.current_thread().name

        logger.info("{} start!".format(current_name))

        while self.status == self.EngineStatus.RUNNING:
            # task_priority其实就是search rule中指定的优先级
            task_priority, task = self.get_task_from_queue()

            # 预先过滤一次hash值，如果已经泄露的表中存在这样的hash，跳过后续的检查
            # 可能会有漏报
            # 某文件已经命中规则A，存入表中
            # 当匹配规则B时，会导致跳过匹配该文件
            # result = self.check_hash(task)

            # 获取所有需要filter的规则，先全局filter，再子filter
            all_filter_rules: List[GeyeFilterRuleModel] = self.get_filter_rules(task["srid"])
            logger.debug("Get all filter rules: {}".format(all_filter_rules))

            # 获取完整的代码
            response_result = self.get_raw_code(task["full_code_url"])
            if not response_result["success"]:
                # 失败了，把任务重新放回队列
                # 这里可能导致worker卡死
                self.put_task_to_queue(target_queue=self.filter_task_queue, task=(task_priority, task))
                logger.debug("Re-put done. continue.")
                continue
            raw_code = response_result["code"]

            # 按照规则开始匹配
            logger.debug("#### [start] SEARCH RULE: {}".format(task["search_rule_name"]))
            logger.debug("#### Content URL: {}".format(task["full_code_url"]))
            for _rule in all_filter_rules:
                logger.debug("==== filter rule: {}, content: {}".format(_rule, _rule.rule))
                result = self.do_filter(_rule, task, raw_code)

                # 匹配过程中有错误，直接终止匹配
                if not result or result["error"]:
                    break

                # 根据规则的正向/反向，获取是否命中
                # hit变量表示是否命中规则
                if _rule.rule_type == 1:
                    # 正向匹配，匹配到算命中
                    hit = True if result["found"] else False
                elif _rule.rule_type == 2:
                    # 反向匹配，没有匹配到算命中
                    hit = True if not result["found"] else False
                else:
                    logger.error("Error rule_type: {}".format(_rule.rule_type))
                    break
                logger.debug("filter end. hit result: %s", hit)

                # 根据匹配结果，决定是向下匹配还是存起来
                if hit:
                    _action = _rule.action
                    # 1-啥也不做，继续下一条匹配，不保存，可以用于其他规则的前置
                    # 2-设为误报，结束匹配，不保存，可以排除掉一定不是敏感信息泄露的内容
                    # 3-设为误报，结束匹配，保存，可以排除掉一定不是敏感信息泄露的内容
                    # 4-设为确认，结束匹配，保存，确定规则
                    # 5-设为待确认，结束匹配，保存
                    if _action == 1:
                        logger.debug("Action: None -> continue next.")
                        continue
                    elif _action == 2:
                        logger.debug("Action: Ignore -> no save -> end filter.")
                        break
                    elif _action == 3:
                        logger.debug("Action: Ignore -> save -> end filter.")
                        save_task = (task_priority, {
                            "code": result["code"],
                            "status": LeaksStatusConstant.IGNORE,
                            "pushed": 0,
                            "frid": _rule.id,
                            "filter_task": task,
                            "filter_rule_name": _rule.name
                        })
                        self.put_task_to_queue(save_task, target_queue=self.save_task_queue)
                    elif _action == 4:
                        logger.debug("Action: Confirm -> save -> end filter.")
                        save_task = (task_priority, {
                            "code": result["code"],
                            "status": LeaksStatusConstant.CONFIRM,
                            "pushed": 0,
                            "frid": _rule.id,
                            "filter_task": task,
                            "filter_rule_name": _rule.name
                        })
                        self.put_task_to_queue(save_task, target_queue=self.save_task_queue)
                    elif _action == 5:
                        logger.debug("Action: To-be-confirmed -> save -> end filter.")
                        save_task = (task_priority, {
                            "code": result["code"],
                            "status": LeaksStatusConstant.TO_BE_CONFIRMED,
                            "pushed": 0,
                            "frid": _rule.id,
                            "filter_task": task,
                            "filter_rule_name": _rule.name
                        })
                        self.put_task_to_queue(save_task, target_queue=self.save_task_queue)
                    else:
                        logger.error("Unknown action value: {}".format(_action))
                else:
                    logger.debug("no hit, continue filter next rule.")
                    continue

            logger.debug("#### [end] SEARCH RULE: {}".format(task["search_rule_name"]))

        logger.info("{} end!".format(current_name))
