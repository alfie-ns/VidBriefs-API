#!/bin/bash

# Load environment variables
load_env() {
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    else
        echo ".env file not found."
        exit 1
    fi
}

load_env

# Activate virtual environment
if source venv/bin/activate; then
    # Start Django server
    echo "Starting Django server..."
    if python manage.py runserver; then # if server started successfully
        echo -e "\nServer started\n."
    else # if server failed to start
        echo -e "\nFailed to start the Django server.\n"
        exit 1 # 1 indicates an error
    fi
else # if virtual environment failed to activate
    echo -e "\nFailed to activate the virtual environment.\n"
    exit 1 # safe exit
fi