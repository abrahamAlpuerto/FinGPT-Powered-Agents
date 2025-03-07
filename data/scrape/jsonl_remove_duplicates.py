import json

def remove_duplicates(input_file, output_file):
    unique_lines = set()
    duplicate_count = 0
    
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    for line in lines:
        json_obj = json.loads(line)
        json_str = json.dumps(json_obj, sort_keys=True)
        if json_str in unique_lines:
            duplicate_count += 1
        else:
            unique_lines.add(json_str)
    
    with open(output_file, 'w') as outfile:
        for unique_line in unique_lines:
            json_obj = json.loads(unique_line)
            json.dump(json_obj, outfile)
            outfile.write('\n')
    
    print(f"Number of duplicate lines found: {duplicate_count}")

file_name = 'essays_of_warren_buffett'
input_file = f'../train/{file_name}.jsonl'
output_file = f'../train/{file_name}.jsonl'
remove_duplicates(input_file, output_file)
