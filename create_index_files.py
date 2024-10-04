import configparser
import json
import os
from openai import OpenAI

# Constants
__CONTENT_DIR = "data/mds_without_refs"
__OUTPUT_DIR = "data/indexes"
__CONTENT_PROMPT_LENGTH = 200

prompt = """You are a highly professional editor specializing in wilderness and disaster medicine. Your task is to create a JSON-formatted structured index of the provided Turkish text. Ignore Markdown syntax like bullet points and links but consider headers for context. Minimum length of the index to 25 terms. Follow these strict criteria:

a. Terms relevant to wilderness and disaster medicine.
b. Terms are frequently used within the text.
c. Terms that are specific and precise.
d. Suggest related terms for cross-referencing.
e. Accommodate professional-level reader comprehensio
f. Maintain consistency, organization, and comprehensiveness.
g. Include proper names where applicable.

The JSON format should be as follows:
{
    "1": {
        "term": "<term>",
        "related_terms": [],
        "context": []
    },
    ...
}

The text to be indexed is:
"""

config_parser = configparser.ConfigParser()
config_parser.read("openaiconfig.ini")
openai_api_key = config_parser["keys"]["openaikey"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Get list of files to process
files_to_parse = os.listdir(__CONTENT_DIR)

# Iterate through each markdown file in the content directory
for mdfile in sorted(files_to_parse):
    if not mdfile.endswith(".md"):
        continue
    print(f"Processing file: {mdfile}")
    base_file_name = os.path.splitext(mdfile)[0]

    # Parse file into sections based on header markers
    sections = []
    current_section = {"title": "", "contents": []}
    with open(os.path.join(__CONTENT_DIR, mdfile)) as f:
        for line in f:
            if not line.startswith("# "):
                if line != "\n":
                    current_section["contents"].append(line)
            else:
                sections.append(current_section)
                current_section = {"title": line[2:], "contents": []}
        sections.append(current_section)

    # Process each section of the file
    section_number = 1
    for section in sections:
        if (len(section["contents"])) < 5:
            continue
        print(f"Section: {section['title'].strip()} ({len(section['contents'])} lines)")
        section_parts = [
            section["contents"][
                i * __CONTENT_PROMPT_LENGTH : (i + 1) * __CONTENT_PROMPT_LENGTH
            ]
            for i in range(
                (len(section["contents"]) + __CONTENT_PROMPT_LENGTH - 1)
                // __CONTENT_PROMPT_LENGTH
            )
        ]
        print(f"Number of parts: {len(section_parts)}")

        lines = 0
        for part in section_parts:
            if not os.path.exists(__OUTPUT_DIR):
                os.mkdir(__OUTPUT_DIR)
            outfile = os.path.join(
                __OUTPUT_DIR,
                f"{base_file_name}-{section_number:02d}-{''.join(x for x in section['title'] if x.isalnum())}-{lines:04d}-{(lines+len(part)):04d}",
            )
            if not os.path.exists(outfile + ".json"):
                print("Calling OpenAI API...")
                text = "".join(part)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text},
                    ],
                )

                print("Writing output files...")
                # Save relevant API response data
                response_data = {
                    "id": response.id,
                    "created": response.created,
                    "model": response.model,
                    "choices": [
                        {
                            "index": choice.index,
                            "message": {
                                "role": choice.message.role,
                                "content": choice.message.content
                            },
                            "finish_reason": choice.finish_reason
                        }
                        for choice in response.choices
                    ]
                }
                with open(outfile + ".txt", "w") as f:
                    f.write(json.dumps(response_data, indent=2))

                result = response.choices[0].message.content
                try:
                    # Clean the result to remove any leading or trailing JSON markers
                    cleaned_result = result.strip()
                    if cleaned_result.startswith("```json"):
                        cleaned_result = cleaned_result[7:]
                    if cleaned_result.endswith("```"):
                        cleaned_result = cleaned_result[:-3]
                    # Convert the cleaned JSON string to a Python object
                    result_json = json.loads(cleaned_result)
                    # Convert the Python object back to a JSON string and write it to the file
                    with open(outfile + ".json", "w", encoding="utf-8") as f:
                        json.dump(result_json, f, ensure_ascii=False, indent=4)
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON returned for {outfile}. Saving raw content.")
                    with open(outfile + ".json", "w", encoding="utf-8") as f:
                        f.write(result)
            else:
                print(f"Output file {outfile}.json already exists, skipping.")

            lines += len(part)
            section_number += 1

    print("File processing complete.\n")