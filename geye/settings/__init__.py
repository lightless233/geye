#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
import os

from .settings_default import *

if os.environ.get("GEYE_ENV") == "prod":
    from .settings_prod import *
elif os.environ.get("GEYE_ENV") == "dev":
    from .settings_dev import *
else:
    from .settings_dev import *
