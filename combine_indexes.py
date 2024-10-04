"""
    Combines multiple index JSON files into a master index.
"""

import json
import os

# Directory where individual index files are stored
__OUTPUT_DIR = 'data/indexes'

def is_valid_index_json(index_part: dict) -> bool:
    """
    Validates the structure of an index JSON part.

    Args:
        index_part (dict): A part of the index to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    for key in index_part:
        if not key.isdigit():
            return False
        if not int(key) in range(1, 50):
            return False
        value = index_part[key]
        if not isinstance(value, dict):
            return False
        if "term" not in value:
            return False
        if not isinstance(value['term'], str):
            return False
        if "related_terms" not in value:
            return False
        if not isinstance(value['related_terms'], list):
            return False
        if "context" not in value:
            return False
        if not isinstance(value['context'], list):
            return False
    return True

# List all files in the output directory
files_to_parse = os.listdir(__OUTPUT_DIR)
master_index = {}

# Iterate through each file in a sorted order
for index_file in sorted(files_to_parse):
    if not index_file.endswith('.json'):
        continue  # Skip non-JSON files

    print(f"loading: {index_file}")
    base_file_name = os.path.splitext(index_file)[0]
    print(base_file_name)
    try:
        # Open and load the JSON content of the current index file
        with open(os.path.join(__OUTPUT_DIR, index_file)) as f:
            index_part = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {index_file}: {e}")
        continue  # Skip files that cannot be loaded

    # Iterate through each term in the current index part
    for index_number, index_term in index_part.items():
        term = index_term['term']
        context = {'reference': base_file_name, 'context': index_term['context']}
        related_terms = index_term['related_terms']

        # Perform a case-insensitive check for existing term in master_index
        matching_key = next((key for key in master_index if key.lower() == term.lower()), None)

        if matching_key:
            # If term exists, append the new context
            master_index[matching_key]['context'].append(context)
            
            # Merge related terms, ensuring no duplicates
            master_index[matching_key]['related_terms'] = list(set(master_index[matching_key]['related_terms'] + related_terms))
        else:
            # If term doesn't exist, add it to the master_index
            master_index[term] = {'context': [context], 'related_terms': related_terms}

# Notify that the master index file is being written
print("writing master index file")
with open("data/master_index.json", "w", encoding="utf-8") as f:
    # Sort the master_index keys case-insensitively
    sorted_master_index = dict(sorted(master_index.items(), key=lambda x: x[0].lower()))
    # Dump the sorted master index to a JSON file with indentation for readability
    json.dump(sorted_master_index, f, indent=2, ensure_ascii=False)