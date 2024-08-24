#!/bin/bash

# Vidbriefs/vidbriefs-api/cp-api.sh

# Function to copy contents of a directory
copy_directory() {
    local dir=$1
    find "$dir" -type f \( -name "*.py" -o -name "*.html" -o -name "*.js" -o -name "*.css" \) -exec echo "File: {}" \; -exec cat {} \; -exec echo \; >> "$temp_file"
}

# Temporary file to store combined output
temp_file=$(mktemp)

# List of available apps
apps=("accounts" "cp" "django" "git" "main" "markdown" "phone" "run" "start-up" "ted_talks" "venv" "youtube")

# Ask user which apps to copy
echo "Available apps:"
for i in "${!apps[@]}"; do 
    echo "$((i+1)). ${apps[$i]}"
done
echo "$((${#apps[@]}+1)). All apps"

read -p "Enter the numbers of the apps you want to copy (space-separated) or 'all': " choices

if [[ "$choices" == "all" ]]; then
    for app in "${apps[@]}"; do
        echo -e "\n--- $app ---\n" >> "$temp_file"
        copy_directory "$app"
    done
else
    for choice in $choices; do
        if (( choice > 0 && choice <= ${#apps[@]} )); then
            app=${apps[$((choice-1))]}
            echo -e "\n--- $app ---\n" >> "$temp_file"
            copy_directory "$app"
        fi
    done
fi

# Add contents of manage.py
echo -e "\n--- manage.py ---\n" >> "$temp_file"
cat manage.py >> "$temp_file"

# Copy the combined contents to clipboard
cat "$temp_file" | pbcopy

# Clean up
rm "$temp_file"

echo "Contents of selected apps and manage.py have been copied to clipboard."