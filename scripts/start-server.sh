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
source venv/bin/activate

# Start Django server
echo "Starting Django server..."
python manage.py runserver

echo "Server started."