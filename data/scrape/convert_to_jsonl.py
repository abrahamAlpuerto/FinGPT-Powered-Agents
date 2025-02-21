import json
import re

def convert_to_jsonl(input_file, output_file):
    """Convert a well formatted question/answer text file to jsonl file"""
    data = []

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex pattern to capture questions and answers
    qa_pairs = re.findall(r'\*\*\d+\.\s(.*?)\*\*\s*(.*?)\n\n(?=\*\*\d+\.|$)', content, re.DOTALL)

    instruction = "Answer the following question based on your knowledge of finance and Warren Buffett."

    for question, answer in qa_pairs:
        data.append({'context': f'Instruction: {instruction}\nInput: {question}', 'target': answer})

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(f'{json.dumps(entry, ensure_ascii=False)}\n')

convert_to_jsonl('wikipedia_data.txt', '../train/wikipedia_data.jsonl')
convert_to_jsonl('warren_buffett_letters.txt', '../train/warren_buffett_letters.jsonl')
convert_to_jsonl('essays-of-warren-buffett.txt', '../train/essays_of_warren_buffett.jsonl')
