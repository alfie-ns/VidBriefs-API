#!/bin/bash

# run this API on DigitalOcean VM

# Define the name of the API application and the port it should run on
API_NAME="vidbriefs-api"
PORT=8000

# Function to start the application
start_api() {
    # Restart the Django development server
    # 'nohup' runs the command immune to hangups, with output redirected to /dev/null
    # '&' at the end runs the process in the background
    # '> /dev/null 2>&1' redirects both standard output and standard error to /dev/null
    nohup python manage.py runserver 0.0.0.0:$PORT > /dev/null 2>&1 & 
    
    # Print a message indicating that the API has been started
    echo "$API_NAME started on port $PORT"
}

# Check if the application is already running
# 'pgrep -f' searches for a process by its full command line
# '> /dev/null' suppresses the output of pgrep
if pgrep -f "$API_NAME" > /dev/null
then
    # If the process is found, print a message
    echo "$API_NAME is running"
else
    # If the process is not found, start the application
    echo "$API_NAME is not running. Starting it now."
    start_api
fi

# Check if the port is already in use
# 'nc' (netcat) is used to check if the port is open
# '-z' tells nc to just scan for listening daemons, without sending any data
# '!' negates the condition, so the block runs if the port is NOT in use
if ! nc -z localhost $PORT; then
    # If the port is not in use, print a message and start the application
    echo "Port $PORT is not in use. Starting $API_NAME"
    start_api
else
    # If the port is in use, print a message
    echo "Port $PORT is already in use."
fi