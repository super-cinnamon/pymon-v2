#!/bin/bash

# Install dependencies listed in requirements.txt
if [ ! -f "requirements.txt" ]; then
  echo "Error: requirements.txt not found!"
  exit 1
fi

pip install -r requirements.txt

# Run the Python script
python run.py

# Exit with the script's exit code (if available)
exit $
