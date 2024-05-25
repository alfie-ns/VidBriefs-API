#!/bin/bash

python3 -m venv venv #create new venv
source venv/bin/activate #activate venv
pip3 install -r requirements.txt #install required dependencies

echo "Setup complete"
ech