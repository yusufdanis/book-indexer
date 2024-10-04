"""
    Converts all PDF files in a specified directory to Markdown format using a shell script.
"""

import os
import subprocess
import concurrent.futures

def convert_pdf_to_md_shell(pdf_path, md_path, crop_amount, language):
    """
    Converts a single PDF file to Markdown using the convert_pdf_to_md.sh shell script.

    Args:
        pdf_path (str): Path to the input PDF file.
        md_path (str): Path where the output Markdown file will be saved.
        crop_amount (int): Amount to crop from the PDF during conversion.
        language (str): Language settings for the conversion.
    """
    script_path = './convert_pdf_to_md.sh'
    try:
        # Execute the shell script with the provided arguments
        subprocess.run([script_path, pdf_path, md_path, str(crop_amount), language], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_path} to {md_path}: {e}")

def convert_all_pdfs(input_dir='data/pdfs', output_dir='data/mds', crop_amount=100, language='tur+eng'):
    """
    Converts all PDF files in the input directory to Markdown format using a shell script.

    Args:
        input_dir (str): Directory containing PDF files to convert.
        output_dir (str): Directory where converted Markdown files will be saved.
        crop_amount (int): Amount to crop from the PDF during conversion.
        language (str): Language settings for the conversion.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List all PDF files in the input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

    # Use a ThreadPoolExecutor to handle multiple conversions concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in pdf_files:
            pdf_path = os.path.join(input_dir, filename)
            md_filename = os.path.splitext(filename)[0] + '.md'
            md_path = os.path.join(output_dir, md_filename)
            print(f"Submitting conversion task for {filename}...")
            # Submit the conversion task to the executor
            futures.append(executor.submit(convert_pdf_to_md_shell, pdf_path, md_path, crop_amount, language))
        
        # Iterate through completed futures to catch any exceptions
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Conversion task generated an exception: {e}")

    print("All PDFs have been converted to Markdown.")

if __name__ == "__main__":
    # Execute the conversion process when the script is run directly
    convert_all_pdfs()