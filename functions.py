#! /usr/bin/env python3
import requests as r
from pygbif import species as sp


def main():
    get_conservation_status(["Quercus suber"])


# query function to get a specific species' IUCN conservation status
def get_conservation_status(checklist):
    # initialize dictionary that will save all of the conservation statuses
    iucn = {}
    # loop through all species names
    for species in checklist:
        # querying Keys
        taxonomyKeys = sp.name_backbone(name=species)
        speciesKey = taxonomyKeys["usageKey"]

        # some species data isn't available through pygbif, so we will use requests \n
        # to fetch such data. For this we the need api url for each species:
        url = f"https://api.gbif.org/v1/species/{speciesKey}/iucnRedListCategory"

        stat = r.get(url)
        stat.encoding = "utf-8"  # Optional: Requests can infer this based on headers.
        payload = stat.json()

        iucn[species] = payload.get("category")

    return iucn


if __name__ == "__main__":
    main()
