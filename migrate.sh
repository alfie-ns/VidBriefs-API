#!/bin/bash
python3 manage.py makemigrations
echo "Migrations created"
python3 manage.py migrate
echo "Migrations applied"