#! /bin/ bash

APP_NAME="vidbriefs-api"
# Check if the application is running
if pgrep -x "$APP_NAME" > /dev/null
then
echo "$APP_NAME is running"
else
echo "$APP_NAME is not running, starting it"
# restart application
python manage.py runserver 0.0.0.0:8000
fi