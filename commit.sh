#!/bin/bash

# Note: This is just a helper script and probably should be replaced with a git hook.

# This script automates the process of committing changes to a Git repository,
# attempts to run a specified Python script using pipper (if available), falls back
# to using python if pipper is not a valid command, and then makes a second commit.
# It requires a commit message as an argument, stages all changed files for commit,
# commits those changes with the provided message, attempts to run the specified Python script,
# and if the script finishes successfully, it makes a second commit with the message "Rebuild".
# Usage: ./run_commit.sh "<commit_message>"

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

# Check if 'pipper' command is available
if command -v pipper >/dev/null 2>&1; then
  # If pipper is available, use it to run the Python script
  pipper run process.py
  pipper_exit_code=$?
else
  # If pipper is not available, fall back to using python
  echo "'pipper' command not found. Falling back to 'python'."
  python process.py
  pipper_exit_code=$?
fi

# If the Python script finishes without errors, commit again with a "Rebuild" message
if [ $pipper_exit_code -eq 0 ]; then
  git commit -am "Rebuild"
else
  echo "Error: Python script did not finish successfully."
  exit 1
fi
