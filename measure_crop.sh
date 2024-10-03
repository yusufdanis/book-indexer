#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 input.pdf"
    exit 1
fi

input_pdf="$1"
output_dir="measure_crop_results"

# Create output directory
mkdir -p "$output_dir"

# Convert first 3 pages of PDF to images
echo "Converting PDF pages to images..."
magick -density 300 "${input_pdf}[0-2]" -quality 100 "$output_dir/page_%01d.png"

# Check if conversion was successful
if [ ! -f "$output_dir/page_0.png" ]; then
    echo "Error: Failed to convert PDF to images."
    echo "Debugging information:"
    echo "PDF file: $input_pdf"
    echo
    exit 1
fi

# Function to perform crop on a single image
perform_crop() {
    local input_image="$1"
    local crop_value="$2"
    local output_image="$3"
    magick "$input_image" -gravity North -chop 0x"$crop_value" -gravity South -chop 0x"$crop_value" -gravity East -chop "$crop_value"x0 -gravity West -chop "$crop_value"x0 "$output_image"
}

# Perform crops for different values
for crop in 50 100 150 200; do
    crop_dir="$output_dir/crop_$crop"
    mkdir -p "$crop_dir"
    
    for page in {0..2}; do
        input_image="$output_dir/page_$page.png"
        if [ -f "$input_image" ]; then
            perform_crop "$input_image" $crop "$crop_dir/page_$page.png"
        else
            echo "Warning: $input_image not found. Skipping..."
        fi
    done
    
    echo "Cropped images with $crop pixels are saved in $crop_dir"
done

# Clean up original images
# rm "$output_dir"/page_*.png

echo "All cropped images are saved in the '$output_dir' directory."
echo "Please review the images in each crop_* subdirectory to determine the best crop value."