import json
import os
import sys

def append_survey_data(input_file, output_folder):
   
    with open(input_file, 'r', encoding='utf-8') as f:
        survey_data = json.load(f)

    
    for survey in survey_data:
        survey_no = survey["Survey No"]
        survey_file = os.path.join(output_folder, f"{survey_no}.json")

        if os.path.exists(survey_file):
           
            with open(survey_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
           
            for key in ["116", "117", "118", "119", "120", "121"]:
                if key in survey:
                    existing_data[key] = survey[key]

           
            with open(survey_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
        else:
            print(f"Survey file {survey_file} does not exist.")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    append_survey_data(input_file, output_folder)
