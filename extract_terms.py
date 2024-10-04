import json

def extract_terms(master_index_file='data/master_index.json', output_file='data/index.txt'):
    """
    Reads the master_index.json file, extracts the terms, sorts them alphabetically,
    and writes them to master_terms.txt with proper capitalization.
    """
    try:
        with open(master_index_file, 'r', encoding='utf-8') as f:
            master_index = json.load(f)
        
        # Extract terms from the JSON structure
        terms = list(master_index.keys())
        
        # Remove any empty strings or None values
        terms = [term for term in terms if term]
        
        # Sort terms alphabetically (case-insensitive)
        terms = sorted(terms, key=lambda x: x.lower())
        
        # Write terms to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for term in terms:
                # Capitalize the first letter of each term
                formatted_term = term[0].upper() + term[1:] if term else ''
                f.write(formatted_term + '\n')
        
        print(f"All terms have been written to {output_file} in alphabetical order.")
    except json.JSONDecodeError:
        print(f"Error: {master_index_file} is not a valid JSON file.")
    except FileNotFoundError:
        print(f"Error: {master_index_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    extract_terms()