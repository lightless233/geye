#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.filter.rule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    规则的filter处理部分

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import multiprocessing
import queue
import shlex
import subprocess
from multiprocessing import Process
from typing import List

import re
from django.conf import settings

from geye.utils.log import logger


class RuleEngine(object):
    """
    filter的部分
    """

    @staticmethod
    def convert_code_to_list(content: str) -> List[str]:
        return content.replace("\r", "\n").split("\n")

    @staticmethod
    def get_neighbor_code(current_no: int, content_array: List[str], offset=5) -> tuple:
        """
        根据当前命中的代码行数，获取前后offset行代码index
        计算的时候是从0开始的，即0行~total-1行
        这样计算方便，不需要考虑下标到实际行数的转换

        :param current_no: 当前命中的行数
        :param offset: 偏移量，默认为5
        :param content_array: 代码文件每一行构成的数组
        :return: tuple(begin_no, end_no, code_array)
        """
        total_no = len(content_array)

        begin_no = current_no - offset
        begin_no = begin_no if begin_no >= 0 else 0

        end_no = current_no + offset
        end_no = end_no if end_no < total_no else total_no

        return begin_no, end_no, content_array[begin_no:end_no]

    @staticmethod
    def _regex_inner_engine(rule: str, code: str, q: multiprocessing.Queue):
        """
        内置regex处理
        :return:
        """
        return_result = {
            "found": False,
            "code": ""
        }
        pattern = re.compile(r"{}".format(rule), re.IGNORECASE)

        # 先按照行迭代匹配，todo: 后续需要优化成只匹配一次
        code_array = RuleEngine.convert_code_to_list(code)
        for line_no, line in enumerate(code_array):
            search_result = pattern.search(line)
            if search_result:
                return_result["has_found"] = True
                begin_no, end_no, code = RuleEngine.get_neighbor_code(line_no, code_array, 5)
                return_result["code"] = "\n".join(code)
                break

        q.put_nowait(return_result)

    @staticmethod
    def _regex_grep_engine(rule: str, code: str):
        """
        grep regex处理器
        :param rule:
        :param code:
        :return:
        """
        return_result = {
            "error": False,
            "found": False,
            "code": ""
        }

        command = "echo {0} | grep -n -i -P {1}".format(code, rule)
        proc = subprocess.Popen(args=command, shell=True, close_fds=True, stdout=subprocess.PIPE)
        try:
            outs = proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            logger.error("[GREP REGEX] filter timeout!")
            proc.kill()
            return_result["error"] = True
            return return_result

        outs = outs[0].strip().decode()
        if not outs:
            return_result["error"] = True
            logger.error("[GREP REGEX] no data from PIPE")
            return return_result
        outs = outs.split(":", 1)
        if len(outs) != 2:
            logger.error("[GREP REGEX] Wrong format outs: {}".format(outs))
            return_result["error"] = True
            return return_result

        # 正常的情况
        line_no = int(outs[0])
        code_array = RuleEngine.get_neighbor_code(line_no, RuleEngine.convert_code_to_list(code), 5)
        return_result["found"] = True
        return_result["code"] = "\n".join(code_array)
        return return_result

    @staticmethod
    def regex_filter(rule_content, filter_content, frid) -> dict:
        # 每次匹配的时候都获取一下，这样可以做到热切换
        regex_engine = settings.REGEX_ENGINE

        # 返回值
        filter_result = {
            "error": False,
            "found": False,
            "code": ""
        }

        if settings.REGEX_ENGINE == "inner":
            # inner engine
            logger.debug("Use 'inner' regex engine.")
            result_queue = multiprocessing.Queue()
            p = Process(target=RuleEngine._regex_inner_engine, args=(rule_content, filter_content, result_queue, ))
            p.start()
            try:
                p.join(60)
                _result = result_queue.get_nowait()
                filter_result["found"] = _result["found"]
                filter_result["code"] = _result["code"]
                return filter_result
            except multiprocessing.TimeoutError:
                # 线程超时
                logger.error("[INNER REGEX] filter timeout! frid: {}".format(frid))
                p.terminate()
                filter_result["error"] = True
                return filter_result
            except queue.Empty:
                # 线程结束了，但是没获取到东西
                logger.error("Empty result get from queue! frid: {}".format(frid))
                filter_result["error"] = True
                return filter_result
        elif settings.REGEX_ENGINE == "grep":
            # grep engine
            rule = shlex.quote(rule_content)
            content = shlex.quote(filter_content)
            _result = RuleEngine._regex_grep_engine(rule, content)
            filter_result["error"] = _result["error"]
            filter_result["found"] = _result["found"]
            filter_result["code"] = _result["code"]
            return filter_result
        else:
            logger.error("Un-support regex-engine '{}' !".format(regex_engine))
            return filter_result

    @staticmethod
    def string_filter(rule_content, filter_content) -> dict:
        """
        普通的字符串in查找
        先通过for迭代查找每一行，todo: 后面需要重构，不然会影响效率
        """
        result = {
            "error": False,
            "found": False,
            "code": ""
        }
        filter_content_array = RuleEngine.convert_code_to_list(filter_content)
        for line_no, line in enumerate(filter_content_array):
            if rule_content in line:
                result["has_found"] = True
                # 取前后各5行代码
                begin_no, end_no, code_array = RuleEngine.get_neighbor_code(line_no, filter_content_array, 5)
                result["code"] = "\n".join(code_array)
                return result

        # 没找到，直接返回result对象
        return result
