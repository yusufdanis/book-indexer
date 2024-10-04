#!/bin/bash

# convert_docx_to_md.sh
# Converts a DOCX file to Markdown format.

# Default CSS file
DEFAULT_CSS="basic.css"

# Help function
usage() {
    echo "Usage: $0 input.docx output.md [stylesheet.css]"
    exit 1
}

# Check required arguments
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    usage
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
CSS_FILE="${3:-$DEFAULT_CSS}"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

# Check if CSS file exists
if [ ! -f "$CSS_FILE" ]; then
    echo "Error: CSS file '$CSS_FILE' not found."
    exit 1
fi

# Run pandoc command
pandoc -c "$CSS_FILE" -f docx "$INPUT_FILE" -t markdown -o "$OUTPUT_FILE"

# Success message
if [ $? -eq 0 ]; then
    echo "Conversion successful: '$INPUT_FILE' -> '$OUTPUT_FILE'"
else
    echo "Error: Conversion process failed."
    exit 1
fi