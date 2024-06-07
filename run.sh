#!/bin/bash

# 1. Create a new virtual environment named 'venv' 
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install the required dependencies from the requirements.txt file
pip3 install -r requirements.txt

# 4. Output a message indicating the start of the database migration
echo "\nMigrating Database"

# 5. Migrate the database (apply all the migrations)
python3 manage.py migrate

# 6. Output a message indicating the start of the superuser creation process
echo "\nCreating Superuser"

# 7. Create a Django superuser (interactive prompt to enter username, email, and password)
python3 manage.py createsuperuser

# 8. Output a message indicating that the setup is complete
echo "\nSetup complete"

# 9. Output a message indicating that the Django server is starting on port 8000
echo "\nStarting Django Server on port 8000"

# 10. Start the Django development server on all available IP addresses (0.0.0.0) and port 8000
python3 manage.py runserver 0.0.0.0:8000
# Run on port 8000, the default for many dev tools, thus ensuring compatibility and reducing conflicts.
