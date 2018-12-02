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
# Web CSRF Token
##########
# CSRF_COOKIE_DOMAIN = "localhost:8080"
# CSRF_USE_SESSIONS = True
CSRF_COOKIE_SAMESITE = None
ALLOWED_CORS = [
    "localhost",
    "127.0.0.1"
]

##########
# Queue settings
##########
# Search任务队列大小
SEARCH_TASK_QUEUE_SIZE = 1024
FILTER_TASK_QUEUE_SIZE = 1024
SAVE_TASK_QUEUE_SIZE = 1024

##########
# Refresh Engine
##########
# 每隔多久检查一次search rule是否需要爬取了
# 默认每隔60秒检查一次每个search rule是否需要爬取了
REFRESH_INTERVAL = 60

##########
# Search Engine
##########
# 设置在爬取的时候是否使用代理
# 如果需要代理，就在下面配置，配置多个代理的情况下
# 每次会随机获取一个代理使用
USE_SEARCH_PROXY = True
SEARCH_PROXIES = [
    {
        "http": "socks5://user:pass@host:port",
        "https": "socks5://user:pass@host:port"
    }
]
# 正则引擎的设置，目前支持的为：
# "inner" - python原生正则引擎，效率较低
# "grep" - linux中的grep命令，效率高，但是windows系统要提前安装才可使用
REGEX_ENGINE = "inner"

##########
# Github API 相关设置
##########
GITHUB_API_SEARCH_URL = "https://api.github.com/search/code"
# 搜索多少页
SEARCH_PAGE_SIZE = 5
# 每页的数量
EACH_PAGE_ITEM_SIZE = 100
