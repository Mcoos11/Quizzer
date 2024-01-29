#!/bin/bash

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn courses.wsgi:application --bind 0.0.0.0:8000