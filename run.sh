#!/bin/bash

if [[ -z "$VIRTUAL_ENV" ]]; then # -z is true if the length of the string is 0, i.e. venv is not active
    echo "Not inside a virtual environment. Exiting with failure." && exit 1
else
    pip install -r requirements.txt
fi

# Ensure scripts are executable
chmod +x scripts/setup-db.sh scripts/run-migrations.sh scripts/start-server.sh

# Setup PostgreSQL role and database
./scripts/setup-db.sh

# Apply Django migrations
./scripts/run-migrations.sh

# Start Django server
./scripts/start-server.sh