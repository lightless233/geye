#!/usr/bin/env bash

SHELL_DIR=$(cd "$(dirname "$0")";pwd)
echo "Shell directory is ${SHELL_DIR}"
cd ${SHELL_DIR}/../
WORK_DIR=`pwd`
echo "Current working directory is ${WORK_DIR}"

PY_ENV_ACTIVATE="${WORK_DIR}/venv/bin/activate"
GUNICORN_CONFIG="${WORK_DIR}/conf/gunicorn_config.py"


source "${PY_ENV_ACTIVATE}"

gunicorn \
    -c ${GUNICORN_CONFIG} \
    --env DJANGO_SETTINGS_MODULE=geye.settings \
    geye.wsgi
