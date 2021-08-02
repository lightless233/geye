#!/usr/bin/env bash

echo "========== Starting geye =========="
echo "========== Apply database migrations =========="
python manage.py migrate

echo "========== Starting Web Service =========="
gunicorn -c /app/geye/conf/gunicorn_config.py \
  --env DJANGO_SETTINGS_MODULE=geye.settings \
  geye.wsgi

echo "========== Starting Agent Service =========="
python manage.py run --single

echo "========== Shell sleep =========="
# just keep this script running
while true; do
    sleep 1
done
