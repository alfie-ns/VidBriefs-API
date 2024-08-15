#!/bin/bash

cd ..

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

# Function to create a new table
create_table() {
    echo -n "Enter table name: "
    read table_name
    echo -n "Enter table schema (e.g., id SERIAL PRIMARY KEY, name VARCHAR(50)): "
    read table_schema
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE TABLE IF NOT EXISTS $table_name ($table_schema);"
    if [ $? -eq 0 ]; then
        echo "Table $table_name created successfully."
    else
        echo "Failed to create table $table_name."
    fi
}

# Function to drop a table
drop_table() {
    echo -n "Enter table name to drop: "
    read table_name
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "DROP TABLE IF EXISTS $table_name;"
    if [ $? -eq 0 ]; then
        echo "Table $table_name dropped successfully."
    else
        echo "Failed to drop table $table_name."
    fi
}

# Function to list all tables
list_tables() {
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "\dt"
}

# Function to backup the database
backup_db() {
    PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F c -b -v -f "$DB_NAME.backup" $DB_NAME
    if [ $? -eq 0 ]; then
        echo "Database $DB_NAME backed up successfully."
    else
        echo "Failed to backup database $DB_NAME."
    fi
}

# Interactive shell
while true; do
    echo "Select an option:"
    echo "1) Create a new table"
    echo "2) Drop a table"
    echo "3) List all tables"
    echo "4) Backup the database"
    echo "5) Exit"
    echo -n "Enter choice [1-5]: "
    read choice
    case $choice in
        1) create_table ;;
        2) drop_table ;;
        3) list_tables ;;
        4) backup_db ;;
        5) exit 0 ;;
        *) echo "Invalid option. Please enter a number between 1 and 5." ;;
    esac
done