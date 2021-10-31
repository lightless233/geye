#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    result.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from django.db import models


class GeyeYuqueLeakManager(models.Manager):
    pass


class GeyeYuqueLeaksModel(models.Model):
    class Meta:
        db_table = "geye_yuque_leaks"

    # 语雀文档的标题
    title = models.CharField(max_length=512, default="No Title")

    # 文档的URL，是跳转形式，并非直接链接
    # 也许可以用来去重
    go_url = models.CharField(max_length=512, default="")

    # 直链 URL
    url = models.CharField(max_length=2048, default="")

    # 知识库名称？
    book_name = models.CharField(max_length=512)

    # 这个知识库所属的 group
    group_name = models.CharField(max_length=512)

    # 文章的摘要信息
    abstract = models.TextField()

    # 标识是哪条搜索规则触发的
    search_rule_id = models.PositiveBigIntegerField(default=0)

    # 这条泄露信息的状态
    # 1 - 待处理，2 - 确认是泄露，3-误报
    status = models.PositiveSmallIntegerField(default=1)

    # 文章的几个时间值
    content_updated_at = models.CharField(max_length=32, default="")
    first_published_at = models.CharField(max_length=32, default="")
    published_at = models.CharField(max_length=32, default="")
    paper_created_at = models.CharField(max_length=32, default="")
    paper_updated_at = models.CharField(max_length=32, default="")

    objects = models.Manager()
    instance = GeyeYuqueLeakManager()
