#! /usr/bin/env python3
import os
import re
import time
from dotenv import load_dotenv, find_dotenv
from Bio import Entrez
from seqtools import querier as q
from seqtools import parser_fasta as fasta
from seqtools import parser_gbk as gbk

print("\n### GENBANK SEQUENCE METADATA FETCHER ###\n")

### SETTING UP ENVIRONMENT VARIABLES ###
# find .env automatically by cycling upstream directories until found
dotenv_path = find_dotenv()
# load entries as environment variables
load_dotenv(dotenv_path)
# define the environment variables
EMAIL = os.getenv("EMAIL")

# beta
def email_input():
    identity = input("Would you like to identify yourself with an email? [y/n]\n")
    match identity:
        case OP, "its me":
            # define the environment variables
            EMAIL = os.getenv("EMAIL")
            return EMAIL
        case y, yes, Yes, YES:
            while True:
                EMAIL = input("Enter your email adress:\n") # add email format checker
                return EMAIL
        case n, no, No, NO:
            return None

# email for identification in ncbi
Entrez.email = EMAIL

def main():
    print("Insert species name list file: ")
    while True:
        try:
            species_file = input("")
            flag = os.path.isfile(species_file)
            if not flag:
                raise FileNotFoundError
            break
        except FileNotFoundError:
            print("Invalid file name. Make sure file the is in the same directory if using relative path.\nPlease try again:")

    print("Select a number for gene: \n1) rbcl;    2) ITS")
    while True:
        try:
            gene_selection = input("")
            match int(gene_selection):
                case 1:
                    gene = "rbcl"
                    break
                case 2:
                    gene = "ITS"
                    break
                case _:
                    print("Invalid input. Please try again: ")
        except ValueError:
            print("Invalid input. Please try again: ")

    print("Select a number for sequence file format: \n 1) fasta;   2) gbk")
    while True:
        try:
            format_selection = input("")
            match int(format_selection):
                case 1:
                    format = "fasta"
                    break
                case 2:
                    format = "gbk"
                    break
                case _:
                    print("Invalid input. Please try again:")
        except ValueError:
            print("Invalid input. Please try again:")

    print("Insert a name for a csv file to output results to: ")
    while True:
        output_filename = input("")
        output_filename = output_filename.lower()
        ext = output_filename[output_filename.rfind("."):]
        if (len(output_filename) <= 255 and                                                     ### Length check
                output_filename.lower() not in ['con', 'prn', 'aux', 'nul'] and                 ### No reserved names
                re.match(r'^[a-zA-Z0-9_\-\\.]+$', output_filename) is not None and              ### No special characters
                not output_filename.startswith('.')):                                           ### No hidden files or directories

            if ext == '.csv' and output_filename:
                output_file = output_filename
                break
            else:
                print("Invalid filename. Please try again:")

    # starting script runtime
    start = time.perf_counter()

    # calling work functions
    query(
        species_file,               # "checklist.txt"
        gene,                       # "rbcl"
        format
    )
    parse(
        ".inttemp",
        output_file,
        format
    )
    # deleting intermediary temp file
    os.remove(".inttemp")
    # ending script runtime
    end = time.perf_counter()

    print(f"It took {float(end - start)} seconds to run this script!")

def query(species_file, gene, format):
    # assign variables here
    # species_file = "checklist.txt"  # text file with species names to be queried
    # gene = "rbcl"                   # barcode, e.g. ITS, rbcL, trnL, ITS1, ITS2, matK, etc
    # _format = "fasta"               # format style queried, can be fasta, gbk or xml
    num_matches = 10                  # max nº of seq matches per species
    # run the functions
    matches = q.entrezSearch(species_file, gene, num_matches)
    q.entrezFetch(format, matches)

def parse(input, output_file, format):
    if format == "fasta":
        fasta.previewFasta(input)
        parsed_data = fasta.parseFasta(input)
        fasta.csv_write(parsed_data, output_file)
    elif format == "gbk":
        gbk.previewgbk(input)
        parsed_data = gbk.parsegbk(input)
        gbk.csv_write(parsed_data, output_file)

main()
