#!/bin/bash

python manage.py makemigrations
python manage.py migrate --noinput

gunicorn courses.wsgi:application --bind 0.0.0.0:8000