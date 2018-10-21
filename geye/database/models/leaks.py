#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.leaks
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    存储抓取到的泄露内容

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from django.db import models

from geye.database.models.base import GeyeBaseModel


class LeaksStatusConstant:
    TO_BE_CONFIRMED = 1
    CONFIRM = 2
    IGNORE = 3


class GeyeLeaksModel(GeyeBaseModel):
    """

    repo name
        仓库的名称
    author
        仓库作者
    path
        完整的文件路径，带文件名的
    filename
        文件名
    sha:
        sha256 hash
    full_code_url
        完整代码路径 raw.github.com/xx
    url:
        github上的url地址
    code
        命中规则的代码段
    search rule id
        SRID 命中的search规则ID
    filter rule id
        FRID 命中的filter规则ID，如果没有命中任何filter rule，则为0
    status
        这个信息当前的状态，1-待处理，2-已确认是泄露，3-误报
    pushed
        预留字段，是否已经推送到其他系统，1-已推送到其他系统，0-未推送到其他系统
    """

    class Meta:
        db_table = "geye_leaks"

    repo_name = models.CharField(max_length=256, default="", db_index=True)
    author = models.CharField(max_length=256, default="")
    path = models.CharField(max_length=1024, default="")
    filename = models.CharField(max_length=256, default="")
    sha = models.CharField(max_length=40, default="", db_index=True)
    full_code_url = models.TextField()
    url = models.TextField()
    code = models.TextField()
    srid = models.BigIntegerField(default=0)
    frid = models.BigIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=1)
    pushed = models.BooleanField(default=False)
