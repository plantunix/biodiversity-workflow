import os
import csv
import time
import json as j

import requests as r
import pandas as pd
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
    basis_of_record = ['LIVING_SPECIMEN', 'LIVING_SPECIMEN', 'HUMAN_OBSERVATION']
    backbone = "testing_backbone.txt"
    occ_search(basis_of_record)
    #reconcile(".tempocc", backbone)
    #download(dataset_filter, basis_of_record)

def dataset_filter():

    # first, static occurrence dataset filter embedded in url (using requests because pygbif severely lacks features):
    print("Fetching datasets...")

    api_url = "https://api.gbif.org/v1/dataset/search?"     # api endpoint
    params = {
        'type' : 'OCCURRENCE',
        'offset' : 0,
        'limit' : 10#1000
    }

    full_data = []

    while api_url:
        datasets = r.get(api_url, params=params)

        if datasets.status_code == 200 and params['offset'] <= 10:#53000
            # parse json data
            datasets = datasets.json()
            # extract results and add data to full dataset list
            full_data.extend(datasets['results'])
            # incrementing offset number
            params['offset'] += 1000
            print(".")
        elif params['offset'] > 10:#53000
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


def occ_search(basis_of_record=None, keys=dataset_filter()):
    # column names
    print('taxonName,taxonRank,lat,lon', file=open('.tempocc', "w"))
    countries = ["PT", "ES"]

    # third, cycle through each dataset key extracted earlier
    for key in keys:
        # offset, limit and rate limit specification
        offset = 0
        limit = 100#300
        rate_limit = 0.05

        # pagination loop until there are no more occurrences to fetch
        while True:
    # fourth, setup filters: plant (taxonKey=6), dataset key, country, coordinate and basis of record and get query
            dataset = occ.search(
                taxonKey = 6,
                datasetKey = key,
                country = countries,
                hasCoordinate = True,
                hasGeospatialIssue = False,
                basisOfRecord = basis_of_record,
                offset = offset,
                limit=limit
            )

            # break if there are no more occurrences to fetch
            if dataset.get('endOfRecords', False) or dataset.get('count', 0) == 0:
                break

    # fifth, for each entry in a call, take taxa name and rank, lat and lon and print to disk

            for oc in dataset['results']:
                if oc.get('taxonRank') == "FAMILY":
                    # get family taxon name
                    taxa = (
                        oc.get('family')
                    ).strip()
                if oc.get('taxonRank') == "GENUS":
                    # get genus taxon name
                    taxa = (
                        oc.get('genus')
                    ).strip()
                if oc.get('taxonRank') in ["SPECIES", "SUBSPECIES"]:
                    # get taxa full name by concatenating generic, specific and infraspecific names
                    taxa = (
                    oc.get('genericName') + ' ' +
                    oc.get('specificEpithet') + ' ' +
                    oc.get('infraspecificEpithet', ' ')
                    ).strip()
                else:
                    continue

                # get taxonRank
                rank = (
                    oc.get('taxonRank')
                )

                # get location data
                lat = oc.get('decimalLatitude')
                lon = oc.get('decimalLongitude')

                # write data in temporary file
                print(f'{taxa}, ' + f'{rank}, ' + f'{lat}, ' + f'{lon}', file=open('.tempocc', "a"))

                # rate limiting
                time.sleep(rate_limit)

            # update the offset for next batch
            offset += limit


# import protection
if __name__ == "__main__":
    main()
