import os
import shutil
import sys
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


def main(inputdir, outputdir, expected=15):
    errors = []
    for file in os.listdir(inputdir):
        basename = os.path.basename(file).replace('.pdf', '')
        os.makedirs(os.path.join(outputdir, basename))
        pdf = convert_from_path(os.path.join(inputdir, file))
        count = 0
        print(file)
        for page in pdf:
            page.save(os.path.join(outputdir, basename, f'{count}.jpg'), 'JPEG')
            count += 1
        if count != expected + 1:
            print(f'Wrong number of pages: {basename}, got: {count - 1} expected: {expected}')
            with open('error.log', 'a') as log:
                log.write(basename)
                log.write('\n')
            error_dir = 'error_old'
            if not os.path.exists('error_old'):
                os.makedirs(error_dir)
            os.rename(os.path.join(inputdir, file), os.path.join(error_dir, file))
            shutil.rmtree(os.path.join(outputdir, basename))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
