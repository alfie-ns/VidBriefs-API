#!/bin/bash

# ------------------------------------ACTIVATE VIRTUAL ENVIRONMENT-------------------------------------
# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    # Remove existing virtual environment
    rm -rf venv
    echo "Creating virtual environment 'venv'..."
    # Create the virtual environment
    python3 -m venv venv
    # Activate the virtual environment
    source venv/bin/activate
else
    echo "Creating virtual environment 'venv'..."
    # Create the virtual environment
    python3 -m venv venv
    # Activate the virtual environment
    source venv/bin/activate
fi # End the if-then statement
# -----------------------------------------------------------------------------------------------------

# ------------------------------------INSTALL REQUIRED PACKAGES----------------------------------------
# Upgrade pip to the latest version
pip install --upgrade pip

# Install required packages from requirements.txt
pip install -r requirements.txt
# The venv holds the required packages for the project
# -----------------------------------------------------------------------------------------------------

# ------------------------------------SETUP DJANGO PROJECT---------------------------------------------
# Migrate the database
echo -e "\nMigrating Database"
python3 manage.py migrate

# Create a superuser for Django admin
echo -e "\nCreating Superuser"
python3 manage.py createsuperuser
# -----------------------------------------------------------------------------------------------------

# ------------------------------------START SERVER-----------------------------------------------------
# Setup is complete
echo -e "\nSetup complete"
# Start the Django server accessible to all IP addresses on port 8000
echo -e "\nStarting Django Server, accessible to all IP addresses on port 8000"
python3 manage.py runserver 0.0.0.0:8000

# -----------------------------------------------------------------------------------------------------

# Deactivate the virtual environment to clean up and avoid conflicts
deactivate