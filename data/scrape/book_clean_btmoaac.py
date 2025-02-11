import PyPDF2
import json
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

import re

def clean_text(text):
    # Fix specific words with \u0000
    replacements = {
        r'Bu\u0000ett\’s': "Buffett's",
        r'Bu\u0000etts': "Buffetts",
        r'Bu\u0000ett': "Buffett",
        r'\u0000ippantly': "flippantly",
        r'\u0000avoring': "favoring",
        r'\u0000lm': "film",
        r'\u0000nancially': "financially",
        r'\u0000e\u0000orts': "efforts",
        r'\u0000ce': "office",
        r'\u0000ect': "effect",
    }

    # Apply replacements
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # Remove remaining null characters
    text = re.sub(r'\u0000', '', text)

    # Normalize spaces and line breaks
    text = re.sub(r'\n', ' ', text)     # Replace line breaks with spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize multiple spaces into a single space

    return text

# Extract text from the PDF
text = extract_text_from_pdf('../books/buffett-the-making-of-an-american-capitalist.pdf')

# Clean the extracted text
cleaned_text = clean_text(text)

# Save the cleaned text to a JSON file
data = {'text': cleaned_text}
with open('../buffett-the-making-of-an-american-capitalist.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Text extracted, cleaned, and saved to 'buffett-the-making-of-an-american-capitalist.json'.")