import os
import time
import json as j

import requests as r
from dotenv import load_dotenv, find_dotenv
from pygbif import occurrences as occ

########################################
### SETTING UP ENVIRONMENT VARIABLES ###
########################################
# find .env automatically by cycling upstream directories until found
dotenv_path = find_dotenv()
# load entries as environment variables
load_dotenv(dotenv_path)
# define the environment variables
GBIF_EMAIL = os.getenv("GBIF_EMAIL")
GBIF_USER = os.getenv("GBIF_USER")
GBIF_PWD = os.getenv("GBIF_PWD")
########################################


def main():
    basis_of_record = ['PRESERVED_SPECIMEN', 'LIVING_SPECIMEN']
    download(basis_of_record)
    #pygbif(basis_of_record)

def download(basis_of_record=None):
    # Default Filters:
        # Keywords in dataset description
        # Basis of Record
        # Plantae Kingdom
        # Country or area
        # Has coordinates
        # Occurrence status

    # first, static occurrence dataset filter embedded in url (using requests because pygbif severely lacks features):
    print("Fetching datasets...")

    api_url = "https://api.gbif.org/v1/dataset/search?"     # api endpoint
    params = {
        'type' : 'OCCURRENCE',
        'offset' : 0,
        'limit' : 1000
    }

    full_data = []

    while api_url:
        datasets = r.get(api_url, params=params)

        if datasets.status_code == 200 and params['offset'] <= 52000:
            # parse json data
            datasets = datasets.json()
            # extract results and add data to full dataset list
            full_data.extend(datasets['results'])
            # incrementing offset number
            params['offset'] += 1000
            print(".")
        elif params['offset'] > 52000:
            # break option 1: offset > count -> download finished
            print(f"Dataset retrieval concluded. Fetched a total of {len(full_data)} datasets.")
            break
        else:
            # break option 2: error in the download
            print(f"Failed to retrieve data. HTTP status code: {datasets.status_code}")
            break

    # second, filter datasets by keywords (excluding occurrences based on genetic data for this case study) and extract keys:
    keywords = ["seq", "sequence", "gene", "DNA", "barcode"]
    keys = []
    for dataset in full_data:
        # apply description-keyword filter
        if not any(keyword.lower() in dataset.get('description', '').lower() for keyword in keywords):
            # put viable dataset keys in a list
            keys.append(dataset['key'])

    print("Applying filters...\n")
    time.sleep(2)  # timer to streamline the interactiveness of the process
    print("Total filtered datasets: ", len(keys))


    ######################
    ## DOWNLOAD REQUEST ##
    ######################

    # third, creating manual dynamic filters for basisOfRecord and former dataset keys for download:

    predicate_datasets = []
    for key in keys:
          predicate_datasets.append({
              "type": "equals",
              "key": "DATASET_KEY",
              "value": key
          })

    predicate_basis = []
    if basis_of_record is not None:
        for basis in basis_of_record:
            predicate_basis.append({
                'type': 'equals',
                'key': 'BASIS_OF_RECORD',
                'value': basis
            })


    # fourth, defining query as a python dict (= json format) / together with plant (taxonKey=6), country, coordinate and occurrence status filters
    query = {
      "creator": GBIF_USER,
      "notificationAddresses": [
          GBIF_EMAIL
      ],
        "sendNotification": True,
        "format": "SIMPLE_CSV",
        "predicate": {
          "type": "and",
          "predicates": [
              {
                          "type": "equals",
                          "key": "TAXON_KEY",
                          "value": "6"
              },
              {
                          "type": "in",
                          "key": "COUNTRY",
                          "values": [ "PT", "ES" ]
              },
              {
                          "type": "equals",
                          "key": "HAS_COORDINATE",
                          "value": "true"
              },
              {
                          "type": "equals",
                          "key": "HAS_GEOSPATIAL_ISSUE",
                          "value": "false"
              },
              {
                          "type": "equals",
                          "key": "OCCURRENCE_STATUS",
                          "value": "PRESENT"
              },
              *predicate_basis,
              *predicate_datasets
            ]
        }
      }

    # convert query into a json string
    query_json = j.dumps(query)

    # API endpoint
    api_url = 'https://api.gbif.org/v1/occurrence/download/request'

    # set the json content type header
    headers = {
       "Content-Type": "application/json"
    }

    # authentication handling
    if GBIF_USER and GBIF_PWD:
        auth = (GBIF_USER, GBIF_PWD)
    else:
        auth = None

    # example curl request structure:
    # curl --include --user userName:PASSWORD --header "Content-Type: application/json" --data @query.json https://api.gbif.org/v1/occurrence/download/request

    # fifth, make the post request
    response = r.post(api_url, headers=headers, data=query_json, auth=auth)

    # take in the server response
    r_code = response.status_code

    # error handling
    if r_code == 201:
        print("HTTP 201: Success!")
    if r_code == 302:
        print("HTTP 302: Found, redirecting...")
    if r_code == 400:
        print("HTTP 400: Bad Request")
    if r_code == 410:
        print("HTTP 410: Gone. No longer available.")

    return r_code # for troubleshooting

def pygbif(basis_of_record): # testing artifact
    datasets = []
    datasets.append('taxonKey = 6')
    for basis in basis_of_record:
        datasets.append(f'basisOfRecord = {basis}')
    print(datasets)

    q = occ.download(format='SIMPLE_CSV', queries=datasets)
    print(q)

# import protection
if __name__ == "__main__":
    main()
