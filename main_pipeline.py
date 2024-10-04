import subprocess
import os
import sys

def run_script(command, description):
    """
    Runs a shell command and handles errors.
    """
    print(f"Starting: {description}...")
    try:
        subprocess.run(command, check=True)
        print(f"Completed: {description}.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")
        sys.exit(1)

def main():
    # Define the scripts and their descriptions
    scripts = [
        #{
        #    'command': ['python', 'create_index_files.py'],
        #    'description': 'Markdown Dosyalarından İndeks Oluşturulması'
        #},
        {
            'command': ['python', 'combine_indexes.py'],
            'description': 'İndeks Dosyalarının Birleştirilmesi'
        },
        {
            'command': ['python', 'extract_terms.py'],
            'description': 'Terimlerin Çıkarılması'
        }
    ]

    # Run each script in order
    for script in scripts:
        run_script(script['command'], script['description'])

    print("Tüm adımlar başarıyla tamamlandı.")

if __name__ == "__main__":
    main()