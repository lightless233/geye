#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    test_monitor_api.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""
import json

import requests


urls = [
    "https://api.github.com/users/Edward-L/events",
    "https://api.github.com/users/lightless233/events",
]


for url in urls:
    resp = requests.get(url)
    result = json.loads(resp.text)

    for _item in result:
        if _item.get("type") == "PushEvent":
            print(_item.keys())
