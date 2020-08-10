import config
import shutil
import requests
import os

api_key = config.dowjones_apikey
# Job ID is the last part of the extraction / snapshot ID.
job_id = config.dowjones_snapshotid
host = "https://api.dowjones.com/alpha/extractions/documents/"
extraction_id = "dj-synhub-extraction-{}-{}".format(api_key, job_id)
target_dir = config.local_download_path

headers = {
    "user-key": api_key,
    "Content-Type": "application/json"
}

response = requests.get(host + extraction_id, headers=headers)
response_json = response.json()
files = response_json["data"]["attributes"]["files"]

print("Starting file download...")

for file in files:
    uri = file["uri"]
    file_name = uri.split("/")[-1]
    file_response = requests.get(uri, headers=headers, allow_redirects=True, stream=True)
    if len(file_name) > 0:
        with open(os.path.join(target_dir, file_name), mode="wb") as local_file:
            file_response.raw.decode_content = True
            shutil.copyfileobj(file_response.raw, local_file)

print("Done.")
