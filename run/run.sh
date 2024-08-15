#!/bin/bash

cd ..

if [[ -z "$VIRTUAL_ENV" ]]; then # -z is true if the length of the string is 0, i.e. venv is not active
    echo "Not inside a virtual environment. Exiting with failure." && exit 1
else
    pip install -r requirements.txt
fi

# Ensure all scripts are executable
chmod +x start-up/setup-db.sh scripts/run-migrations.sh scripts/start-server.sh

# 1. Setup PostgreSQL role and database
./start-up/setup-db.sh && ./scripts/run-migrations.sh && ./scripts/start-server.sh

# 2. Apply Django migrations
./start-up/ripts/run-migrations.sh

# 3. Start Django server
./start-up/start-server.sh