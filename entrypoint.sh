#!/bin/bash

# Run the Python script in an infinite loop
while true; do
  python ./main.py
  echo "Restarting script..."
  sleep 1  # Add a small delay before restarting to avoid rapid restarts in case of immediate failures
done
