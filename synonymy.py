#! /usr/bin/env python3

import requests as r
from pygbif import species as sp

checklist = ["Quercus suber", "Quercus faginea"]


## Synonymy through GBIF ##


def gbif_synonymy(species):
    syn = {}

    for spp in species:
        taxonomy = sp.name_backbone(name=spp)
        speciesKey = taxonomy["usageKey"]

        url = f"https://api.gbif.org/v1/species/{speciesKey}/synonyms?limit=110"

        api = r.get(url)
        api.encoding = "utf-8"
        payload = api.json()

        for i, match in enumerate(payload["results"]):
            syn[spp + " synonym nº" + str(i + 1)] = match["scientificName"]

#    for key, value in syn.items():
#        print(f"{key} : {value}")

    return syn


# Function to get synonyms of a species from POWO
def powo_synonymy(species):
    sin = {}

    # Iterate through each species name
    # for spp in species:
    #    print(f"Fetching synonyms for {species}...")

    query = {Name.genus: "Quercus", Name.species: "suber"}
    results = powo.search(query)

    # pykew lib DOES NOT WORK. OUTDATED. TRY WITH API#
    # search api - https://powo.science.kew.org/api/1/search?q=quercus%20suber
    # taxon api - https://powo.science.kew.org/api/1/taxon/urn:lsid:ipni.org:names:296785-1
    # normal website - https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:296785-1#synonyms


# gbif_synonymy(checklist)
# powo_synonymy(checklist)
