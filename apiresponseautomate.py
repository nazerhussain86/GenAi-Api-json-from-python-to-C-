import os
import requests
import json


# Function to traverse folders and subfolders to find all response.json files
def get_all_response_json_files(folder_path):
    json_files = []
    # os.walk will iterate over all subfolders and files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "responses.json":  # Only look for responses.json
                json_files.append(os.path.join(root, file))
    return json_files


# Function to send file path to the API and log the responses to a txt file
def send_file_path_to_api(api_url, file_path, log_file_path):
    # Construct the request URL with the file path
    params = {'File_Path': file_path}

    # Send GET request to the API
    response = requests.get(api_url, params=params, verify=False)  # Set verify=False for local SSL issues

    # Open log file in append mode with UTF-8 encoding
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"Processing: {file_path}\n")  # Log the file path

        # Check if the response was successful
        if response.status_code == 200:
            try:
                # Try to parse and pretty-print the JSON response
                json_response = response.json()
                pretty_json = json.dumps(json_response, indent=4)  # Format JSON with 4 spaces
                log_file.write(f"Success: {file_path} sent to API. Response:\n{pretty_json}\n\n")
            except json.JSONDecodeError:
                # If response is not a valid JSON, try pretty-printing the raw text
                try:
                    raw_json_response = json.loads(response.text)
                    pretty_raw_json = json.dumps(raw_json_response, indent=4)  # Format JSON with 4 spaces
                    log_file.write(f"Success: {file_path} sent to API. Non-JSON Response:\n{pretty_raw_json}\n\n")
                except json.JSONDecodeError:
                    # If it still can't be parsed, write the raw text
                    log_file.write(f"Success: {file_path} sent to API. Non-JSON Response:\n{response.text}\n\n")
            print(f"Success: {file_path} sent to API. Response logged.")
        else:
            log_file.write(
                f"Failed to send {file_path}. Status Code: {response.status_code}, Response:\n{response.text}\n\n")
            print(f"Failed: {file_path}. Status logged with code {response.status_code}.")


# Define the base folder path containing the subfolders
base_folder_path = r'C:\Users\User\Downloads\11.55\11.55'  # Replace with your folder path

# Define the API URL
api_url = 'https://localhost:44354/api/ImpexAPIJsonFormatter/Get'

# Define the path to the log file
log_file_path = r'D:\api_log.txt'  # Adjust the log file path as needed

# Get all response.json files from the base folder
json_files = get_all_response_json_files(base_folder_path)

# Loop through each JSON file and send it to the API
for json_file in json_files:
    print(f"Sending {json_file} to API...")
    send_file_path_to_api(api_url, json_file, log_file_path)
