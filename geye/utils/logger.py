#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""

import logging
import logging.handlers
import os

from django.conf import settings

# 用户配置部分 ↓
LEVEL_COLOR = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}
STDOUT_LOG_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
STDOUT_DATE_FMT = "%Y-%m-%d %H:%M:%S"
FILE_LOG_FMT = "[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
FILE_DATE_FMT = "%Y-%m-%d %H:%M:%S"

# 不同日志级别对用的文件名suffix
LEVEL_SUFFIX = {
    "debug": ".DEBUG",
    "info": ".INFO",
    "warning": ".WARNING",
    "error": ".ERROR",
    "critical": ".CRITICAL",
    "all": ".ALL",
}


# 用户配置部分 ↑

class ColoredFormatter(logging.Formatter):
    COLOR_MAP = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "bg_black": "40",
        "bg_red": "41",
        "bg_green": "42",
        "bg_yellow": "43",
        "bg_blue": "44",
        "bg_magenta": "45",
        "bg_cyan": "46",
        "bg_white": "47",
        "light_black": "1;30",
        "light_red": "1;31",
        "light_green": "1;32",
        "light_yellow": "1;33",
        "light_blue": "1;34",
        "light_magenta": "1;35",
        "light_cyan": "1;36",
        "light_white": "1;37",
        "light_bg_black": "100",
        "light_bg_red": "101",
        "light_bg_green": "102",
        "light_bg_yellow": "103",
        "light_bg_blue": "104",
        "light_bg_magenta": "105",
        "light_bg_cyan": "106",
        "light_bg_white": "107",
    }

    def __init__(self, fmt, datefmt):
        super(ColoredFormatter, self).__init__(fmt, datefmt)

    def parse_color(self, level_name):
        color_name = LEVEL_COLOR.get(level_name, "")
        if not color_name:
            return ""

        color_value = []
        color_name = color_name.split(",")
        for _cn in color_name:
            color_code = self.COLOR_MAP.get(_cn, "")
            if color_code:
                color_value.append(color_code)

        return "\033[" + ";".join(color_value) + "m"

    def format(self, record):
        record.log_color = self.parse_color(record.levelname)
        message = super(ColoredFormatter, self).format(record) + "\033[0m"

        return message


class FileLoggerFilter(logging.Filter):
    """
    用来过滤输出到文件中的日志
    只有当当期的日志级别和指定的级别一致时，才输出
    """

    def __init__(self, level: str):
        super(FileLoggerFilter, self).__init__()
        self.level = level.upper()

    def filter(self, record: logging.LogRecord):
        """
        Is the specified record to be logged? Returns zero for no, nonzero for yes.
        :param record:
        :return:
        """
        if self.level == "all":
            return True
        else:
            return record.levelname == self.level


class LoggerFactory(object):
    """
    from utils.logger import LoggerFactory
    logger = LoggerFactory.get_logger(__name__)
    """

    log_to_file = settings.LOG_TO_FILE
    log_filename = settings.LOG_FILENAME
    log_level = settings.LOG_LEVEL if settings.LOG_LEVEL else "DEBUG"

    @classmethod
    def get_logger(cls, name):
        _logger = logging.getLogger(name)

        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(
            ColoredFormatter(
                fmt=STDOUT_LOG_FMT,
                datefmt=STDOUT_DATE_FMT,
            )
        )
        _logger.addHandler(stdout_handler)

        if cls.log_to_file:
            # 检查指定的日志目录是否存在，如果不存在就先创建目录
            _tmp_path = settings.LOG_PATH
            if not os.path.exists(_tmp_path):
                os.mkdir(_tmp_path)
            _tmp_path = os.path.join(_tmp_path, cls.log_filename)

            # 写文件的handler
            file_formatter = logging.Formatter(fmt=FILE_LOG_FMT, datefmt=FILE_DATE_FMT)
            file_handler = logging.handlers.TimedRotatingFileHandler(_tmp_path, when="midnight", backupCount=15)
            file_handler.setFormatter(file_formatter)
            _logger.addHandler(file_handler)

        _logger.setLevel(cls.log_level)
        return _logger
