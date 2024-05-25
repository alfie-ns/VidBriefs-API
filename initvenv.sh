#!/bin/bash

python3 -m venv venv #create new venv
source venv/bin/activate #activate venv
pip3 install -r requirements.txt #install required dependencies

echo "Setup complete"
echo "Starting Django Server on port 8000"

python3 manage.py runserver 0.0.0.0:8000 


