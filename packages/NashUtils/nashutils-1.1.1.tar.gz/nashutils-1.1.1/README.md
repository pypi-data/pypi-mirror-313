#  NashUtils

NashUtils is a lightweight, versatile Python utility library designed to simplify everyday programming tasks. It provides a collection of tools and modules to handle data manipulation, file conversions, and other common utility functions, helping developers streamline their workflows and write cleaner, more efficient code.

# Features
## CSV_TO_JSON
- Converts CSV files to JSON format with ease.
- Handles large datasets.
- Simple and lightweight implementation.
## CreateGitBranch
- creates a git branch 
- shows the craeted branch 
- switches to the branch 
## PythonPackageCleanUP
- **This is only for windows**
- removes the dist/* folder and other folder craeted from python bulid cmd 
## PythonPackageUpload
- Bulids and Uploads the Python files to PyPi 
- Make sure you copy your API key under account settings 
# Usage
- Clone the repository:
  ```bash
      git clone https://github.com/yourusername/csv-to-json-converter.git

- Download depedencies 
  ```bash
      pip install -r requirements.txt

- Running the CSV_to_JSON class
  ```bash
  from Utils.CSV_to_JSON import csv_to_json
  
  Convetor = csv_to_json
  CSV = 'data.csv'
  JSON = 'data.json'
  Convetor.run(CSV,JSON)

- Running the CreateGitBranch
    ```bash 
    from Utils.CreateGitBranch import CreateGitBranch
    CreateGitBranch.run()

- Running the PythonPackageCleanUP
    ```bash 
    from Utils.PythonPackageCleanUP import PythonPackageCleanUP
    PythonPackageCleanUP.run()

- Running the PythonPackageUploads
    ```bash 
    from Utils.PythonPackageUploads import PythonPackageUploads
    PythonPackageUploads.run()

