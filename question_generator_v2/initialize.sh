#!/bin/bash

gunicorn question_generator_v2.wsgi:application --bind 0.0.0.0:8000