#!/bin/bash

# Create a new virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies from the requirements.txt file
pip3 install -r requirements.txt

# Output a message indicating the start of the database migration
echo "\nMigrating Database"

# Migrate the database (apply all the migrations)
python3 manage.py migrate

# Output a message indicating the start of the superuser creation process
echo "\nCreating Superuser"

# Create a Django superuser (interactive prompt to enter username, email, and password)
python3 manage.py createsuperuser

# Output a message indicating that the setup is complete
echo "\nSetup complete"

# Output a message indicating that the Django server is starting on port 8000
echo "\nStarting Django Server on port 8000"

# Start the Django development server on all available IP addresses (0.0.0.0) and port 8000
python3 manage.py runserver 0.0.0.0:8000