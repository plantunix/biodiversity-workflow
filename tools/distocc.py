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
    # Default Filters:
        # Keywords in dataset description
        # Basis of Record
        # Plantae Kingdom
        # Country or area
        # Has coordinates
        # Occurrence status
    basis_of_record = ['PRESERVED_SPECIMEN', 'LIVING_SPECIMEN']
    occ_search()
    #download(dataset_filter, basis_of_record)
    #pygbif(basis_of_record)

def dataset_filter(basis_of_record=None):

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

        if datasets.status_code == 200 and params['offset'] <= 1000:
            # parse json data
            datasets = datasets.json()
            # extract results and add data to full dataset list
            full_data.extend(datasets['results'])
            # incrementing offset number
            params['offset'] += 1000
            print(".")
        elif params['offset'] > 1000:
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

    return keys


def occ_search(keys=None, basis_of_record=None):

    # third, cycle through each dataset key extracted earlier
    #for key in keys:
        # pagination loop until there are no more occurrences to fetch
        while True:
            # offset and limit specification
            offset = 0
            limit = 300

    # fourth, setup filters: plant (taxonKey=6), dataset key, country, coordinate and basis of record and get query
            dataset = occ.search(
                taxonKey = 6,
                datasetKey = "4cf3eec1-b902-40c9-b15b-05c5fe5928b6",#key,
                country = "PT",#, ES"],
                hasCoordinate = True,
                hasGeospatialIssue = False,
                basisOfRecord = 'HUMAN_OBSERVATION',#basis_of_record[0]
                offset = offset,
                limit=5
            )

    # fifth, for each entry in a call, take taxa name, lat and lon and print to disk
            for oc in dataset['results']:

                # get taxa full name by concatenating generic, specific and infraspecific names
                taxa = (
                oc.get('genericName') + ' ' +
                oc.get('specificEpithet') + ' ' +
                oc.get('infraspecificEpithet', ' ')
                ).strip()

                # get location data
                lat = oc.get('decimalLatitude')
                lon = oc.get('decimalLongitude')

                # write data in temporary file
                print(taxa + ", " + str(lat) + ", " + str(lon), file=open('.tempocc', "a"))

                print(taxa, lat, lon)

            # break if there are no more occurrences to fetch
            more = (oc.get('genericName', '') for oc in dataset['results'])
            if not more:
                break

            # update the offset for next batch
            offset += limit


# import protection
if __name__ == "__main__":
    main()
