# !/bin/bash

# Make this file executable: chmod +x run-web.sh
# Run it with: ./run-web.sh
# Both commands: chmod +x run-web.sh && ./run-web.sh

# Check if the virtual environment activation script exists
# (typical path on Windows)
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
# Otherwise, check the typical path for Unix/Linux/macOS
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
# If neither activation script is found
else
    # Print an error message
    echo "Virtualenv not found"
    # Exit the script with an error code
    exit 1
fi

#export FLASK_APP=user_interface/web/webapp.py
export FLASK_APP=user_interface.webapp
export PYTHONPATH=$(pwd)

flask run