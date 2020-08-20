import requests
import json
import os

import config
from time import sleep

USER_KEY = config.dowjones_apikey

# The URL of the Extractions Endpoint
url = 'https://api.dowjones.com/alpha/extractions/documents'

headers = {'content-type': 'application/json', 'user-key': USER_KEY}

request_body = {
    "query": {
    "where": "(REGEXP_CONTAINS(LOWER(CONCAT(title,' ',snippet,' ',body)), r'(\\b)(tourism|bed\\W+and\\W+breakfast\\W+inns|campgrounds|rv\\W+parks|hotels|motels|casino\\W+hotels|online\\W+tourism\\W+reservation\\W+services|scenic|sightseeing\\W+services|tour\\W+operators|travel\\W+agencies|transportation|logistics|air\\W+transport|airlines|air\\W+freight|chartered\\W+air\\W+freight|passenger\\W+airlines|chartered\\W+passenger\\W+airlines|low\\W+cost\\W+airlines|airports|leisure|travel\\W+goods|luggage|travel\\W+insurance|travel\\W+reviews|travel|cruises|luxury\\W+travel|travel\\W+deals|packages|travel\\W+reviews|travel\\W+deals|packages)(\\b)') OR REGEXP_CONTAINS(LOWER(industry_codes), r'(^|,)(itourm|i6653|i6654|i6651|i6652|i7505|i761|i765|i77001|itsp|iairtr|i75|i7502|i7504|i7501|i7503|ilowair|i764|ilgood|i442|itvlins|gtrrw)($|,)') OR REGEXP_CONTAINS(LOWER(subject_codes), r'(^|,)(gtour|gcrui|gluxtr|gtdeal|gtrrw|gtdeal)($|,)')) AND language_code='en' AND publication_date >= '2019-01-01 00:00:00'"
    }
}

# Create an explain with the given query
print("Creating an explain: " + json.dumps(request_body))
response = requests.post(url + "/_explain", data=json.dumps(request_body), headers=headers)

# Check the explain to verify the query was valid and see how many docs would be returned
if response.status_code != 201:
    print("ERROR: An error occurred creating an explain: " + response.text)
else:
    explain = response.json()
    print("Explain Created. Job ID: " + explain["data"]["id"])
    state = explain["data"]["attributes"]["current_state"]

    # wait for explain job to complete
    while state != "JOB_STATE_DONE":
        self_link = explain["links"]["self"]
        response = requests.get(self_link, headers=headers)
        explain = response.json()
        state = explain["data"]["attributes"]["current_state"]

    print("Explain Completed Successfully.")
    doc_count = explain["data"]["attributes"]["counts"]
    print("Number of documents returned: " + str(doc_count))

    print("Proceed with the Snapshot? (Y/N)")
    proceed = input('>')

    if proceed.lower() != 'y' and proceed.lower() != "yes":
        print("Not proceeding with extraction")
    else:
        # Create a Snapshot with the given query
        print("Creating the Snapshot: " + json.dumps(request_body))
        response = requests.post(url, data=json.dumps(request_body), headers=headers)
        print(response.text)

        # Verify the response from creating an extraction is OK
        if response.status_code != 201:
            print("ERROR: An error occurred creating an extraction: " + response.text)
        else:
            extraction = response.json()
            print(extraction)
            print("Extraction Created. Job ID: " + extraction['data']['id'])
            self_link = extraction["links"]["self"]
            sleep(30)
            print("Checking state of the job.")

            while True:
                # We now call the second endpoint, which will tell us if the extraction is ready.
                status_response = requests.get(self_link, headers=headers)

                # Verify the response from the self_link is OK
                if status_response.status_code != 200:
                    print("ERROR: an error occurred getting the details for the extraction: " + status_response.text)
                else:
                    # There is an edge case where the job does not have a current_state yet. If current_state
                    # does not yet exist in the response, we will sleep for 10 seconds
                    status = status_response.json()

                    if 'current_state' in status['data']['attributes']:
                        currentState = status['data']['attributes']['current_state']
                        print("Current state is: " + currentState)

                        # Job is still running, Sleep for 10 seconds
                        if currentState == "JOB_STATE_RUNNING":
                            print("Sleeping for 30 seconds... Job state running")
                            sleep(30)

                        elif currentState == "JOB_VALIDATING":
                            print("Sleeping for 30 seconds... Job validating")
                            sleep(30)

                        elif currentState == "JOB_QUEUED":
                            print("Sleeping for 30 seconds... Job queued")
                            sleep(30)

                        elif currentState == "JOB_CREATED":
                            print("Sleeping for 30 seconds... Job created")
                            sleep(30)

                        else:
                            # If currentState is JOB_STATE_DONE then everything completed successfully
                            if currentState == "JOB_STATE_DONE":
                                print("Job completed successfully")
                                print("Downloading Snapshot files to current directory")
                                for file in status['data']['attributes']['files']:
                                    filepath = file['uri']
                                    parts = filepath.split('/')
                                    filename = parts[len(parts) - 1]
                                    r = requests.get(file['uri'], stream=True, headers=headers)
                                    dir_path = config.local_download_path
                                    filename = os.path.join(dir_path, filename)
                                    with open(filename, 'wb') as fd:
                                        for chunk in r.iter_content(chunk_size=128):
                                            fd.write(chunk)

                            # Job has another state that means it was not successful.
                            else:
                                print("An error occurred with the job. Final state is: " + currentState)

                            break
                    else:
                        print("Sleeping for 30 seconds...")
                        sleep(30)
