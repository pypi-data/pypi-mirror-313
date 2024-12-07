import csv
import json

class csv_to_json():
    def __init__(self):
        pass
    
    def run(CSBC_file_path,JSON_file_path):

        # Read CSV and convert to JSON
        with open(CSBC_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]

        with open(JSON_file_path, mode='w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"CSV file has been converted to JSON and saved as {JSON_file_path}")