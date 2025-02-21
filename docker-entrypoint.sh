#!/bin/sh

python manage.py collectstatic --noinput

if [ "$DJANGO_RUN_MIGRATE" = "1" ]
then
  python manage.py migrate --no-input
fi

exec gunicorn _conf.wsgi --bind=0.0.0.0:8080