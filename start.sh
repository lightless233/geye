#!/usr/bin/env bash

source ./venv/bin/activate

gunicorn \
    -c ./conf/gunicorn_config.py \
    --env DJANGO_SETTINGS_MODULE=geye.settings \
    geye.wsgi
