#!/bin/bash
SCRIPT_FILE="run.py"

# run
echo "Running script $SCRIPT_FILE ..."

chmod +x "$SCRIPT_FILE"

python "$SCRIPT_FILE"

echo "stop running script $SCRIPT_FILE ..."
