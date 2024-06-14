#!/bin/bash

# ------------------------------------CONFIGURE DATABASE VARIABLES-------------------------------------
DB_NAME="your_db_name"           # Replace with your actual database name
DB_USER="your_db_user"           # Replace with your actual database user
DB_PASSWORD="your_db_password"   # Replace with your actual database password
DB_HOST="localhost"              # Database host, typically localhost for local development

# Export password for non-interactive use
export PGPASSWORD=$DB_PASSWORD

# ------------------------------------CREATE DATABASE AND USER-----------------------------------------
# Log in to PostgreSQL as the default 'postgres' superuser
echo -e "\nCreating database and user..."

psql -h $DB_HOST -U postgres <<EOF
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
      CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASSWORD';
   ELSE
      RAISE NOTICE 'Role "$DB_USER" already exists. Skipping creation.';
   END IF;
END
\$\$;

DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME') THEN
      CREATE DATABASE $DB_NAME;
      GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
   ELSE
      RAISE NOTICE 'Database "$DB_NAME" already exists. Skipping creation.';
   END IF;
END
\$\$;
EOF
# -----------------------------------------------------------------------------------------------------

echo -e "\nDatabase setup complete. Please ensure your Django settings.py is updated with the following configuration:"

echo -e "\nRun migrations and create a superuser as necessary."

# Unset the password for security reasons
unset PGPASSWORD
