#!/bin/bash

# Function to load environment variables from .env file
load_env() {
    if [ -f .env ]; then
        while IFS='=' read -r key value; do
            # Trim spaces and quotes
            key=$(echo "$key" | sed 's/^ *//; s/ *$//')
            value=$(echo "$value" | sed 's/^ *//; s/ *$//; s/^"//; s/"$//')
            # Export variable safely
            if [[ $key && ! $key =~ ^# ]]; then
                export "$key=$value"
            fi
        done < .env
    else
        echo ".env file not found."
        exit 1
    fi
}

# Load environment variables
load_env

# Check if PostgreSQL is running
if ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
    echo "PostgreSQL is not running."
    exit 1
fi

# Connect to the database using psql
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME