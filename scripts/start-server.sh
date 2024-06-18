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
        echo "Server started."
    else # if server failed to start
        echo "Failed to start the Django server."
        exit 1 # 1 indicates an error
    fi
else # if virtual environment failed to activate
    echo "Failed to activate the virtual environment."
    exit 1 # safe exit
fi