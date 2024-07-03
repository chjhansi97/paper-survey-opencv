import csv
import json
import sys

def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return value
    
def csv_to_json(csv_file_path, json_file_path):
    data = []
    
    with open(csv_file_path, newline='', encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            row["Survey No"] = convert_to_int(row["Survey No"])
            row["117"] = convert_to_int(row["117"])
            row["118"] = convert_to_int(row["118"])
            row["119"] = convert_to_int(row["119"])
            data.append(row)
    
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    csv_file_path = sys.argv[1]  
    json_file_path = sys.argv[2]  
    
    csv_to_json(csv_file_path, json_file_path)
    print(f'CSV data has been converted to JSON and saved to {json_file_path}')
