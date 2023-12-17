#!/bin/bash

python manage.py migrate
python manage.py collectstatic

gunicorn authentication.wsgi:application --bind 0.0.0.0:8000