import os
import glob
import re

def clean_text(text):
    """Handle special characters and formatting"""
    # Normalize line endings and handle special characters
    text = text.replace('\r\n', '\n').replace('\r', '\n')  # Normalize newlines
    text = text.replace('\x0c', '\n\n')                    # Replace form feeds
    text = text.replace('-\n', '')                         # Remove hyphenated line breaks
    return text

def process_single_file(input_path, output_path, encoding='utf-8'):
    """Process a single file into single-line format"""
    try:
        with open(input_path, 'r', encoding=encoding) as in_f:
            content = clean_text(in_f.read())
            
            # Convert to single line format
            single_line = content.replace('\n', ' ')
            single_line = re.sub(r'\s+', ' ', single_line).strip()
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding=encoding) as out_f:
                out_f.write(single_line + '\n')
                
        print(f"Successfully processed: {os.path.basename(input_path)}")
        return True
    
    except Exception as e:
        print(f"⚠️ Error processing {os.path.basename(input_path)}: {str(e)}")
        return False

def batch_process_files(input_dir, output_dir, encoding='utf-8'):
    """Process all .txt files in a directory"""
    try:
        input_dir = os.path.abspath(input_dir)
        output_dir = os.path.abspath(output_dir)
        
        print(f"\n{'='*40}\nInput Directory: {input_dir}\nOutput Directory: {output_dir}\n{'='*40}")

        if not os.path.isdir(input_dir):
            raise ValueError(f"Input directory does not exist: {input_dir}")
            
        txt_files = glob.glob(os.path.join(input_dir, '*.txt'))
        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in {input_dir}")
            
        print(f"Found {len(txt_files)} text files to process\n")
        
        successful = 0
        for i, txt_file in enumerate(txt_files, 1):
            output_path = os.path.join(output_dir, os.path.basename(txt_file))
            if process_single_file(txt_file, output_path, encoding):
                successful += 1
                
        print(f"\n{'='*40}\nProcessing complete!\nSuccessfully processed: {successful}/{len(txt_files)}")
        print(f"Output directory: {output_dir}\n{'='*40}")

    except Exception as e:
        print(f"\n{'❌'*10}\nCritical Error: {str(e)}\n{'❌'*10}")
        raise

# Configuration - Use absolute paths
input_directory = '/Users/dmv62/FinLoRA-Agent/data/books/'
output_directory = '/Users/dmv62/FinLoRA-Agent/data/onelineperdoctxts/processed/'

# Run the processor
batch_process_files(
    input_dir=input_directory,
    output_dir=output_directory
)