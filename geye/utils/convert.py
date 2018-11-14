#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.utils.convert
    ~~~~~~~~~~~~~~~~~~

    一些通用的数据格式转换类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime


class CommonConvert:
    @staticmethod
    def datetime_to_str(d: datetime.datetime):
        return d.strftime("%Y-%m-%d %H:%M:%S")
