#!/bin/bash

# Ensure scripts are executable
chmod +x scripts/setup-db.sh scripts/run-migrations.sh scripts/start-server.sh

# Setup PostgreSQL role and database
./scripts/setup-db.sh

# Apply Django migrations
./scripts/run-migrations.sh

# Start Django server
./scripts/start-server.sh