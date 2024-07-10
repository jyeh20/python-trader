#!/bin/bash

PATH_TO_VENV="../"
PATH_TO_REQUIREMENTS="./requirements.txt"
PATH_TO_STOCK_ANALYZER="../stock_analysis.py"

# Get the day of the week (1 for Monday, ..., 7 for Sunday)
DOW=$(date +%u)

# Check if the day is a weekday (Monday=1 to Friday=5)
if [ "$DOW" -ge 1 ] && [ "$DOW" -le 5 ]; then
    # Check if virtual environment directory exists
    if [ ! -d $PATH_TO_VENV ]; then
        # Create virtual environment
        python3 -m venv $PATH_TO_VENV
        # Activate virtual environment and install dependencies
        source $PATH_TO_VENV/bin/activate
        pip install -r $PATH_TO_REQUIREMENTS
        deactivate
    fi
    # Activate virtual environment
    source $PATH_TO_VENV/bin/activate
    # Launch the Python script
    python $PATH_TO_STOCK_ANALYZER
    # Deactivate virtual environment
    deactivate
else
    echo "Today is not a weekday. The script will not run."
fi
