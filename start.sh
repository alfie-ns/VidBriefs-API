#!/bin/bash

# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    # Activate the virtual environment
    source venv/bin/activate
else
    echo "Creating virtual environment 'venv'..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

echo -e "\nMigrating Database"
python3 manage.py migrate

echo -e "\nCreating Superuser"
python3 manage.py createsuperuser

echo -e "\nSetup complete"
echo -e "\nStarting Django Server on port 8000"
python3 manage.py runserver 0.0.0.0:8000

# Deactivate the virtual environment
deactivate