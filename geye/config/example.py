#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.config.dev
    ~~~~~~~~~~~~~~~~~~

    样例配置文件
    使用时将该文件复制一份，并根据不同的环境进行命名，目前支持三种
    cp ./example.py ./dev.py
    cp ./example.py ./pre.py
    cp ./example.py ./prod.py

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

# import os
# import base64

DEBUG = True
# SECRET_KEY = base64.b64encode(os.urandom(32))
SECRET_KEY = "g6FeurQ+dFKg76zPifuoORS0v2vQZ6i38dXRtIvQM+Y="

# LOG信息配置，其中LOG_PATH为log存放的位置，基于BASE_DIR（项目当前路径）的相对路径
LOG_TO_FILE = True
LOG_FILENAME = "geye.log"
LOG_PATH = "./logs/"

# 允许访问的来源HOST
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

# pgsql 数据库配置
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""

##########
# Queue settings
##########
# Search任务队列大小
SEARCH_TASK_QUEUE_SIZE = 1024

##########
# Refresh Engine
##########
# 每隔多久检查一次search rule是否需要爬取了
# 默认每隔60秒检查一次每个search rule是否需要爬取了
REFRESH_INTERVAL = 60

##########
# Github API 相关设置
##########
GITHUB_API_SEARCH_URL = "https://api.github.com/search/code"
GITHUB_SEARCH_PAGE_SIZE = 5
