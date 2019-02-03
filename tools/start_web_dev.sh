#!/usr/bin/env bash

SHELL_DIR=$(cd "$(dirname "$0")";pwd)
echo "Shell directory is ${SHELL_DIR}"
cd ${SHELL_DIR}/../
WORK_DIR=`pwd`
echo "Current working directory is ${WORK_DIR}"

PY_ENV_ACTIVATE="${WORK_DIR}/venv/bin/activate"

source ${PY_ENV_ACTIVATE}

python manage.py runserver 0.0.0.0:10001
