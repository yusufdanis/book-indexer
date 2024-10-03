#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 input.pdf output.md crop_amount language"
    echo "Example: $0 input.pdf output.md 100 tur+eng"
    exit 1
fi

input_pdf="$1"
output_md="$2"
crop_amount="$3"
language="$4"
temp_dir=$(mktemp -d)

# Set TESSDATA_PREFIX if needed
# export TESSDATA_PREFIX="/usr/share/tessdata"

# Convert PDF to images, enhancing color contrast
magick -density 300 "$input_pdf" -normalize -level 20%,80%,1 -quality 100 "$temp_dir/page_%03d.png"

# Perform OCR on images and combine results
for img in "$temp_dir"/*.png; do
    # Crop the image to remove headers and footers
    magick "$img" -gravity North -chop 0x"$crop_amount" -gravity South -chop 0x"$crop_amount" -gravity East -chop "$crop_amount"x0 -gravity West -chop "$crop_amount"x0 "$img"
    
    # Add white border to make it easier for OCR
    magick "$img" -bordercolor White -border 20 "$img"
    
    # Run Tesseract
    tesseract "$img" "$img" -l "$language"
done

cat "$temp_dir"/*.txt > "$temp_dir/combined.txt"

# Post-process the text to improve Markdown formatting
awk '
    # If line is in all caps and not too long, treat as a heading
    length($0) > 0 && length($0) <= 100 && $0 == toupper($0) {
        print "## " $0
        next
    }
    
    # Otherwise, print the line as is
    { print }
' "$temp_dir/combined.txt" > "$temp_dir/formatted.txt"

# Convert to Markdown
pandoc -f markdown -t markdown_strict "$temp_dir/formatted.txt" -o "$output_md"

# Clean up
rm -r "$temp_dir"

echo "Conversion completed: $output_md has been created."