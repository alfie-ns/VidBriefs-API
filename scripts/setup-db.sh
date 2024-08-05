#!/bin/bash

# Function to load environment variables from .env file
load_env() {
    if [ -f .env ]; then
        while IFS='=' read -r key value; do
            if [[ $key && ! $key =~ ^# ]]; then
                # Remove leading/trailing spaces and quotes from the value
                value=$(echo "$value" | sed 's/^ *//; s/ *$//; s/^"//; s/"$//')
                # Export variable safely
                export "$key=$value"
            fi
        done < .env
    else
        echo ".env file not found."
        exit 1
    fi
}

# ---

# 0. Load environment variables
load_env

# 1. Ensure PostgreSQL service is running
if ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
    echo "Starting PostgreSQL service..."
    brew services start postgresql
fi

# 2. Create the superuser role if not exists
psql -h $DB_HOST -p $DB_PORT -d template1 -U $(whoami) <<EOF
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = '$(whoami)') THEN
        CREATE ROLE "$(whoami)" WITH SUPERUSER LOGIN PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;
EOF

# 3. Create PostgreSQL role if it doesn't exist
psql -h $DB_HOST -p $DB_PORT -d template1 -U $(whoami) <<EOF
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = '$DB_USER') THEN
        CREATE ROLE "$DB_USER" WITH LOGIN PASSWORD '$DB_PASSWORD';
        ALTER ROLE "$DB_USER" CREATEDB;
    END IF;
END
\$\$;
EOF

# 4. Create the database if it doesn't exist
psql -h $DB_HOST -p $DB_PORT -d template1 -U $(whoami) -c "
SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1 || psql -h $DB_HOST -p $DB_PORT -d template1 -U $(whoami) -c "CREATE DATABASE \"$DB_NAME\" OWNER \"$DB_USER\";"

echo -e "\nDatabase setup complete.\n"