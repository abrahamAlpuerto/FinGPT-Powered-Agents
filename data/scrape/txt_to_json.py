import json
import re

filename = "Schroeder_The-Snowball-.txt"

dict1 = {}

# Read the content of the file
with open(filename, 'r', encoding='utf-8') as fh:
    dict1["text"] = fh.read()  # Read the entire content of the file

def clean_text(text):
    # Remove remaining null characters
    text = re.sub(r'\u0000', '', text)
    text = re.sub(r'\u00b7', '', text)
    text = re.sub(r'\u2019', '\'', text)
    
    
    # Normalize spaces and line breaks
    text = re.sub(r'\n', ' ', text)     # Replace line breaks with spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize multiple spaces into a single space

    return text

dict1["text"] = clean_text(dict1['text'])

# Save the dictionary as a JSON file
output_file = "../Schroeder_The-Snowball-.json"
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(dict1, out_file, indent=4, sort_keys=False)

print(f"Text saved to {output_file}")

