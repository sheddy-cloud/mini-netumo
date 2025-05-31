#!/bin/bash

# Set base path
base_dir="$(pwd)"
frontend_dir="$base_dir/frontend"

# Collect valid CSS files relative to frontend/
css_files=()

for abs_path in "$@"; do
  # Only include .css files
  if [[ "$abs_path" == *.css && "$abs_path" == "$frontend_dir"* ]]; then
    rel_path="${abs_path#$frontend_dir/}"  # Trim the leading frontend/
    css_files+=("$rel_path")
  fi
done

# Exit if no CSS files are found
if [ ${#css_files[@]} -eq 0 ]; then
  exit 0
fi

# Now cd into frontend and run stylelint
cd "$frontend_dir" || exit 1
npx stylelint --fix "${css_files[@]}"
