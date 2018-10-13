#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.token
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    存储github搜索用的token

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models

from .base import GeyeBaseModel


class GeyeTokenModel(GeyeBaseModel):
    """
    token:
        github access token
    remain_limit:
        当前token的剩余可请求次数，从返回头中的X-RateLimit-Remaining获取
        每次搜索的时候，选取这个值最大的，并且更新该值
    status:
        token 状态，1-启用，0-关闭
    """

    class Meta:
        db_table = "geye_token"

    token_name = models.CharField(max_length=32, default="TokenName", null=False)
    token = models.CharField(max_length=64, default="", null=False)
    remain_limit = models.PositiveIntegerField(default=0, null=False)
    status = models.PositiveSmallIntegerField(default=1, null=False)
