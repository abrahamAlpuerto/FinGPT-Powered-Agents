import re

def split_transcripts_by_year(input_file_path):
    current_year_file = None
    current_year = None
    with open(input_file_path, 'r', encoding='utf-8') as f_in:
        for line in f_in:

            match = re.search(r'(Morning|Afternoon) Session - (\d{4}) Meeting', line)
            if match:
                year = match.group(2)
                if year != current_year:
                    if current_year_file:
                        current_year_file.close()
                    output_file_path = f"transcript_{year}.txt"
                    current_year_file = open(output_file_path, 'a', encoding='utf-8')
                    current_year = year



            if current_year_file:
                current_year_file.write(line)



    if current_year_file:
        current_year_file.close()

input_file = 'data\\1-Berkshire-Transcripts-1994-2018.txt' 
split_transcripts_by_year(input_file)

print("Transcripts have been successfully split into yearly files.")