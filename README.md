# loop-survey-digitization

A collection of scripts used for the digitization process of papper surveys for the LOOP-project.

**Note**: These scripts are tailored to fit our purposes (identifying checkboxes) for a very specific survey, hence this will unlikely work out of the box if you try to use it without modifying the code

## Extract images from Pdfs
A small util that uses pdf2image for extracting pdf pages to individual jpg-images. So the images can be analysed with opencv

The pdfs original name will be used for naming subfolders containing the extracted images. 

The script should be called with the follwing args: 

* input directory 
* output directory

<pre> python pdf_img_extract.py /path/to/pdf-file-directory /path/to/output-directory </pre>

The script checks for expected number of pages which can be modified in the script. 
If the expected number of pages doesn't math the actual extracted images count the faulty pdf will be moved from the input directory to an error directory.

## Parse the surveys
The script for doing the actual parsing of the surveys. 

The script uses a profile json file which specifies the correct number of questions and is used for controlling how many questions to look for, error checking etc. 

<pre> python pdf_img_extract.py /path/to/directory/with/extracted/images </pre>

When the script runs it will halt if any errors are detected. The correct answers should be noted manually in csv format before proceeding.
When noted or if there was no real error e.g. the answers was actually blank you can press any key to continue the parsing. 
### csv format for manual corrections
<pre>
surevey_id;question_number;answer
12345;45;5
</pre>

### Output

Output will be saved as json files in the same folder as the extracted images. A folder with the processed images will also be saved for audits


### steps to run the scripts
1. <pre>python pdf_img_extract.py scan output </pre> (creates output folder with pdfs extracted to images)
2. <pre>python parse_survey.py output </pre> (creates audit folder(images which are audited or found answers in) and json file with answers for every survey folder)
3. <pre>python move_out_json.py output output_json </pre> (makes a copy of all json files in the output folder)
4. 
