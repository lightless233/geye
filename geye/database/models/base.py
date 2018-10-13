#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Base model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models


class GeyeBaseModel(models.Model):

    class Meta:
        abstract = True

    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
