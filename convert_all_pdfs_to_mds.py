import os
import subprocess
import concurrent.futures

def convert_pdf_to_md_shell(pdf_path, md_path, crop_amount, language):
    """
    Converts a single PDF file to Markdown using the convert_pdf_to_md.sh shell script.
    """
    script_path = './convert_pdf_to_md.sh'  # Shell scriptinizin doğru yolunu belirtin
    try:
        subprocess.run([script_path, pdf_path, md_path, str(crop_amount), language], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_path} to {md_path}: {e}")

def convert_all_pdfs(input_dir='data/pdfs', output_dir='data/mds', crop_amount=100, language='tur+eng'):
    """
    Converts all PDF files in the input directory to Markdown format using a shell script.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in pdf_files:
            pdf_path = os.path.join(input_dir, filename)
            md_filename = os.path.splitext(filename)[0] + '.md'
            md_path = os.path.join(output_dir, md_filename)
            print(f"Submitting conversion task for {filename}...")
            futures.append(executor.submit(convert_pdf_to_md_shell, pdf_path, md_path, crop_amount, language))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Conversion task generated an exception: {e}")
    
    print("All PDFs have been converted to Markdown.")

if __name__ == "__main__":
    convert_all_pdfs()