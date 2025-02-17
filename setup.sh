#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
# Install required libraries
pip install -r requirements.txt


echo "Setup complete."