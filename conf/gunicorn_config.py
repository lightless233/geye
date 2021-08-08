#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    gunicorn_config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Gunicorn的配置文件

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


import multiprocessing

# 是否开启DEBUG模式
_DEBUG = False


# Web后端接口默认开到这个地址
bind = "127.0.0.1:8000"

# workers
# debug模式下只开启1个worker
workers = multiprocessing.cpu_count() * 2 + 1 if not _DEBUG else 1

# worker class
# worker进程的类型，你可能需要手动安装：pip install gunicorn[tornado]
worker_class = "tornado"

# max_requests
# 当worker进程每处理max_requests个请求后，会自动重启，如果为0，则表示永不重启
max_requests = 0
# max_requests_jitter = 0

# worker重启前处理后事的时间
graceful_timeout = 3

# 是否后台运行
# debug模式下不启用
daemon = False if _DEBUG else True

# reload
# 代码变更时是否自动重启，debug模式开启
reload = True if _DEBUG else False
reload_engine = "auto"

# 进程名字
proc_name = "GeyeWeb"

# 请求日志，错误日志，日志格式
accesslog = "./logs/gunicorn/access.log"
errorlog = "./logs/gunicorn/error.log"
# remoteIP - 请求时间 请求行 状态码 返回值长度 "referer" "UA"
access_log_format = '%(h)s %(l)s %(t)s %(r)s %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "debug" if _DEBUG else "info"
capture_output = True
