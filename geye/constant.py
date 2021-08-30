#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    constant
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from enum import unique, IntEnum


@unique
class ResponseCode(IntEnum):
    DEFAULT = -1
    OK = 200
    GENERIC_ERROR = 400
    PARAM_ERROR = 401
    RUNTIME_ERROR = 402

    # 兼容老的code
    OLD_SUCCESS = 1001
    OLD_RUNTIME_ERROR = 1002
    OLD_PARAM_ERROR = 1004
