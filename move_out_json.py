import os
import sys
count = 1
import shutil

def move_json_files(source_directory, target_directory):
    # Create target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.json'):
                # Construct full file path
                file_path = os.path.join(root, file)
                # Move file to target directory
                shutil.copy(file_path, target_directory)

    print('All JSON files have been moved.')

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python move_json_files.py <source_directory> <target_directory>")
        sys.exit(1)

    source_directory = sys.argv[1]
    target_directory = sys.argv[2]

    # Move the JSON files
    move_json_files(source_directory, target_directory)
