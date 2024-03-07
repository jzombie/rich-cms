#!/bin/bash

# Check if a commit message was provided as an argument
if [ $# -eq 0 ]; then
  echo "Error: No commit message provided."
  echo "Usage: $0 <commit_message>"
  exit 1
fi

# Stage the current files
git add .

# Assign the first argument to a variable
commit_message="$1"

# Run git commit with the provided message
git commit -m "$commit_message"

# Run the Python script
# python process.py
pipper run process.py

# If the Python script finishes without errors, commit again with a "Rebuild" message
if [ $? -eq 0 ]; then
  git commit -am "Rebuild"
else
  echo "Error: Python script did not finish successfully."
  exit 1
fi
