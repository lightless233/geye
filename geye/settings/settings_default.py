#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    settings_default
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    默认配置文件，最先加载
    不需要用户配置的内容放到这里

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""

from ._base import BASE_DIR

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # geye app
    'geye.system',
    'geye.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "geye.system.middleware.CORSMiddleware",
    "geye.system.middleware.VueMiddleware",
]

ROOT_URLCONF = 'geye.urls'
WSGI_APPLICATION = 'geye.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/public/'
STATICFILES_DIRS = [
    BASE_DIR / "templates",
]

CSRF_COOKIE_SAMESITE = None
