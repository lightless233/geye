#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    settings_dev.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import os

env = lambda env_name, default_value: \
    os.environ.get(env_name) if os.environ.get(env_name) is not None else default_value

DEBUG = True
SECRET_KEY = "This_is_bad_key"

# LOG信息配置，其中LOG_PATH为log存放的位置，基于BASE_DIR（项目当前路径）的相对路径
LOG_TO_FILE = True
LOG_FILENAME = "geye.log"
LOG_PATH = "./logs/"

# 允许访问的来源HOST
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
ALLOWED_CORS = [
    "localhost",
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME", "GEYE"),
        'USER': env("DB_USER", "GEYE"),
        'PASSWORD': env("DB_PASSWORD", "GEYE"),
        'HOST': env("DB_HOST", "localhost"),
        'PORT': env("DB_PORT", "5432"),
    }
}

##########
# Queue settings
##########
# Search任务队列大小
SEARCH_TASK_QUEUE_SIZE = 1024
FILTER_TASK_QUEUE_SIZE = 1024
SAVE_TASK_QUEUE_SIZE = 1024
MONITOR_TASK_QUEUE_SIZE = 1024
MONITOR_SAVE_QUEUE_SIZE = 1024

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
USE_SEARCH_PROXY = False
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
