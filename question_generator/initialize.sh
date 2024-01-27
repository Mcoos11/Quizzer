#!/bin/bash

gunicorn question_generator.wsgi:application --bind 0.0.0.0:8000