import json
import os

input_folder = "."
output_file = "merged.jsonl"

jsonl_files = [f for f in os.listdir(input_folder) if f.endswith(".jsonl")]

with open(output_file, "w", encoding="utf-8") as outfile:
    for file in jsonl_files:
        file_path = os.path.join(input_folder, file)
        with open(file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)  
