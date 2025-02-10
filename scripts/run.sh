#!/bin/sh

set -e

# first thing to run an app is to wait for the database to be ready otherwise app will be crashed
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
