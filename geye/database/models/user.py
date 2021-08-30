#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    user model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""

from django.db import models

from geye.database.models.base import GeyeBaseModel


class GeyeUserManager(models.Manager):
    pass


class GeyeUserModel(GeyeBaseModel):
    """
    status - 账户状态，0：等待激活，1：正常，2：封禁
    """

    class Meta:
        db_table = "geye_user"

    username = models.CharField(max_length=64, default="", null=False)
    password = models.CharField(max_length=512, default="", null=False)
    email = models.CharField(max_length=128, default="", null=False)
    status = models.PositiveSmallIntegerField(default=0, null=False)

    objects = models.Manager()
    instance = GeyeUserManager()
