#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.core.engine.monitor
    ~~~~~~~~~~~~~~~~~~~~~~~~

    重点仓库监控
    监控指定的用户、仓库、组织下的代码变更

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from django.conf import settings

from geye.core.engine.base import MultiThreadEngine


class MonitorEngine(MultiThreadEngine):

    def __init__(self, app_ctx, name, pool_size=None):
        super(MonitorEngine, self).__init__(app_ctx, name, pool_size)

        # 获取配置信息
        pass

        # 获取代理信息
        self.use_proxy = settings.USE_SEARCH_PROXY
        self.proxies = settings.SEARCH_PROXIES if self.use_proxy else []

        # 获取队列信息


    def _worker(self):
        pass
