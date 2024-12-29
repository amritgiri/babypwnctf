#!/bin/bash

# Function to check if a string is valid Base64
is_base64() {
    echo "$1" | base64 --decode 2>/dev/null | grep -q -P '^\S+$'
}

# Loop through all files in the "files" directory
for file in files/*; do
    # Check if it's a regular file
    if [ -f "$file" ]; then
        echo "==== Decoding: $file ===="
        content=$(cat "$file")
        
        # Check if the content is valid Base64
        if is_base64 "$content"; then
            echo "$content" | base64 -d
        else
            echo "Skipping: $file (Invalid Base64 data)"
        fi
        
        echo -e "\n==========\n"
    else
        echo "Skipping: $file (Not a regular file)"
    fi
done
