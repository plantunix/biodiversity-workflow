#! /usr/bin/env python3
from Bio import Entrez
import time

def main():
    # assign variables here
    species_file = "checklist.txt"  # text file with species names to be queried
    gene = "rbcl"                   # barcode, e.g. ITS, rbcL, trnL, ITS1, ITS2, matK, etc
    _format = "gbk"                 # format style queried, can be fasta, gbk or xml
    num_matches = 5                 # max nº of seq matches per species
    # call the functions
    entrezFetch(_format, entrezSearch(species_file, gene, num_matches))

# email for identification in ncbi
#Entrez.email = EMAIL


# assign list of plant species for seq querying from txt file
def entrezSearch(species_file, gene, num_matches):
    # open the file
    with open(species_file, "r") as file:
        # read all the lines (aka species) from the file
        checklist = file.readlines()

    # search parameters
    retmax = num_matches # results per species
    maxlength = 5000
    matches = {}

    for species in checklist:
        # entrez search query
        query = "{}[Organism] AND {}[Gene] AND 100:{}[SLEN]".format(species, gene, maxlength)
        print("Currently searching for: \n{} sequences from {}".format(gene, species))

        # query NCBI GenBank
        request = Entrez.esearch(db="nucleotide", term=query, retmax=retmax)
        record = Entrez.read(request)
        request.close()

        # store ids
        ids = record["IdList"]
        matches[species] = ids
        print("Found {} sequences.\n".format(len(ids)))

        # NCBI's request rate limiter (3 requests/sec max)
        time.sleep(0.34)

    # search summary
    print("\nSummary of id matches for each species:")
    for species, ids in matches.items():
        print("IDs:{} for {}".format(ids, species))
    return matches

# fetch detailed records in fasta format
def entrezFetch(_format, matches):
    open('output.txt', 'w').close()     #clean the file (needless after the function is streamlined)
    try:
        for species, ids in matches.items():
            if ids:
                fetch = Entrez.efetch(db="nucleotide", id=ids, rettype=_format, retmode="text")
                record = fetch.read()
                fetch.close()
                print("{}".format(record), file=open(".inttemp", "a"))
            time.sleep(0.34)
        print("______________________________//______________________________\n\nData successfully fetched!")
    except Exception as e:
        print(f"______________________________//______________________________\n\nFailed to fetch data: {e}")


if __name__ == "__main__":
    main()
