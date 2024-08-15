#!/bin/bash
cd ..
python manage.py makemigrations
sleep 2
python manage.py migrate
