#!/bin/bash

# ------------------------------------ACTIVATE VIRTUAL ENVIRONMENT-------------------------------------
# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    echo "Activating existing virtual environment 'venv'..."
    # Activate the virtual environment
    source venv/bin/activate
else
    echo "Creating and activating virtual environment 'venv'..."
    # Create the virtual environment
    python3 -m venv venv
    # Activate the virtual environment
    source venv/bin/activate
fi # End the if-then statement
# -----------------------------------------------------------------------------------------------------

# ------------------------------------INSTALL REQUIRED PACKAGES----------------------------------------
# Upgrade pip to the latest version
pip3 install --upgrade pip

# Install required packages from requirements.txt
pip3 install -r requirements.txt
# The venv holds the required packages for the project
# -----------------------------------------------------------------------------------------------------

## ------------------------------------CHECK AND CREATE DATABASE----------------------------------------
## Check if the database exists
#DB_EXISTS=$(psql -h $DB_HOST -U $DB_USER -lqt | cut -d \| -f 1 | grep -w $DB_NAME | wc -l)
#
#if [ "$DB_EXISTS" -eq "0" ]; then
#    echo "Database '$DB_NAME' does not exist. Creating it..."
#    psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
#else
#    echo "Database '$DB_NAME' already exists."
#fi
## -----------------------------------------------------------------------------------------------------

# ------------------------------------APPLY DATABASE MIGRATIONS----------------------------------------
echo -e "\nApplying database migrations"
python3 manage.py migrate
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
