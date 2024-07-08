#!/bin/bash

# Define database file and backup directory
DB_FILE="db.sqlite3"
BACKUP_DIR="db_backups"
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +'%Y%m%d_%H%M%S').sqlite3"

# Ensure the backup directory exists
mkdir -p "$BACKUP_DIR" 


function show_usage {
    echo "Usage: $0 {backup|restore|init|reset|status}"
    echo "    backup  - Create a backup of the database"
    echo "    restore - Restore the database from the latest backup"
    echo "    init    - Initialize the database (run migrations)"
    echo "    reset   - Reset the database to its initial state"
    echo "    status  - Show the current database status"
}

function backup_db {
    echo "Creating backup of the database..."
    cp "$DB_FILE" "$BACKUP_FILE"
    echo "Backup created at $BACKUP_FILE"
}

function restore_db {
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.sqlite3 | head -1)
    if [ -f "$LATEST_BACKUP" ]; then
        echo "Restoring database from $LATEST_BACKUP..."
        cp "$LATEST_BACKUP" "$DB_FILE"
        echo "Database restored from $LATEST_BACKUP"
    else
        echo "No backup found to restore."
    fi
}

function init_db {
    echo "Initializing the database..."
    python manage.py migrate
    echo "Database initialized."
}

function reset_db {
    echo "Resetting the database..."
    rm -f "$DB_FILE"
    init_db
}

function db_status {
    echo "Database status:"
    if [ -f "$DB_FILE" ]; then
        echo "$DB_FILE exists."
        echo "Size: $(du -sh "$DB_FILE" | cut -f1)"
        echo "Backup files:"
        ls -lh "$BACKUP_DIR"
    else
        echo "$DB_FILE does not exist."
    fi
}

if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

case "$1" in
    backup)
        backup_db
        ;;
    restore)
        restore_db
        ;;
    init)
        init_db
        ;;
    reset)
        reset_db
        ;;
    status)
        db_status
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
