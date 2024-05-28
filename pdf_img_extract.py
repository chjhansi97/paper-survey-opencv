import os
import shutil
import sys
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def process_pdf_file(input_file, output_subdir, expected):
    basename = os.path.basename(input_file).replace('.pdf', '')
    output_subdir = os.path.join(output_subdir, basename)
    os.makedirs(output_subdir, exist_ok=True)
    
    try:
        pdf = convert_from_path(input_file)
        count = 0

        for page in pdf:
            page.save(os.path.join(output_subdir, f'{count}.jpg'), 'JPEG')
            count += 1

        if count != expected + 1:
            print(f'Wrong number of pages: {basename}, got: {count - 1}, expected: {expected}')
            with open('error.log', 'a') as log:
                log.write(basename + '\n')

            error_dir = 'error_old'
            os.makedirs(error_dir, exist_ok=True)
            os.rename(input_file, os.path.join(error_dir, os.path.basename(input_file)))
            shutil.rmtree(output_subdir)

    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as e:
        print(f'Error processing file {input_file}: {e}')
        with open('error.log', 'a') as log:
            log.write(f'Error processing file {input_file}: {e}\n')

def main(inputdir, outputdir, expected=15):
    for root, dirs, files in os.walk(inputdir):
        for file in files:
            if file.endswith('.pdf'):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, inputdir)
                output_subdir = os.path.join(outputdir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                process_pdf_file(input_file, output_subdir, expected)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_directory> <output_directory>")
        sys.exit(1)
    
    inputdir = sys.argv[1]
    outputdir = sys.argv[2]
    main(inputdir, outputdir)
