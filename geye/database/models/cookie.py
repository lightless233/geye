#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.cookie
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    cookie 管理表

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from django.db import models

from geye.database.models.base import GeyeBaseModel


class GeyeCookieManager(models.Manager):

    def get_by_domain(self, domain):
        return self.filter(is_deleted=0, domain=domain, status=1).all()


class GeyeCookieModel(GeyeBaseModel):
    class Meta:
        db_table = "geye_cookie"

    # cookie 的名称，用于区分这个 cookie 是干啥用的，并非 cookie 变量的名字
    name = models.CharField(max_length=64, default="cookie name")

    # 这个 cookie 应当被附加到哪个域名上
    domain = models.CharField(max_length=2048, default="")

    # cookie值，可以直接放到 cookie 头中的格式
    # e.g.  _yuque_session=123; _csrf_token=345;
    values = models.TextField()

    # 状态
    # 1：启用，0：关闭
    status = models.PositiveSmallIntegerField(default=1)

    objects = models.Manager()
    instance = GeyeCookieManager()
