#! /usr/bin/env python3
import time
import csv
from Bio import SeqIO
from .utils.refcom import rsearch, csearch
from .utils import featsrx as f


def main():
    # assign file path to parse here: e.g. relative "file" or absolute "/home/user/Documents/file"
    input_file= ".inttemp"
    output_file = "gbk.csv"
    # calling all function
    previewgbk(input_file)
    parsed_data = parsegbk(input_file)
    csv_write(parsed_data, output_file)

# preview function
def previewgbk(input_file):
    # assign list of plant sequences for data parsing from file
    # open the file
    with open(input_file, "r") as file:
        # read all the lines (aka species seq) from the file
        data_list = list(SeqIO.parse(file, "genbank"))
    # preview of the quantity of records identified and small timer
    print("\nFound {} records!".format(len(data_list)))
    time.sleep(1)
    # preview of first and last sequences
    if data_list:
        for i, gbk_record in enumerate(data_list):
            # preview first sequence
            if i == 0:
                print("\nFirst Sequence Record -")
                print("ID:", gbk_record.id, ";  Sequence length:", len(gbk_record.seq), ";  Description:",
                      gbk_record.description)
            # preview last sequence
            elif i == len(data_list)-1:
                print("\nLast Sequence Record -")
                print("ID:", gbk_record.id, ";  Sequence length:", len(gbk_record.seq), ";  Description:",
                      gbk_record.description)
    # clause: something goes wrong with the preview
    else:
        print("No sequence data was found or failed to parse! :(")

# parsing function
def parsegbk(input_file):
    # initialize list object to store useful data
    data = []
    try:
        # assign fasta entry data to dict() form for each sequence,
        # specifying the keys for each entry. Store each dict() as entry in data list()
        for gbk_record in SeqIO.parse(input_file, "genbank"):
            authors, auth1, auth2, auth3, auth4, auth5 = rsearch(gbk_record, "authors")
            title, title1, title2, title3, title4, title5 = rsearch(gbk_record, "title")
            journal, jour1, jour2, jour3, jour4, jour5 = rsearch(gbk_record, "journal")

            info = {
                "id": gbk_record.id,
                "name" : gbk_record.name,
                "length" : str(len(gbk_record.seq))+"bp",
                "locus" : gbk_record.annotations.get('locus'),
                "mol_type" : gbk_record.annotations.get('molecule_type'),
                "topology" : gbk_record.annotations.get('topology'),
                "data_file_div" : gbk_record.annotations.get('data_file_division'),
                "date" : gbk_record.annotations.get('date'),
                "description" : gbk_record.description,
                "definition" : gbk_record.annotations.get('definition'),
                "accession" : gbk_record.annotations.get('accessions'),
                "version1" : str(gbk_record.annotations.get('accessions'))+"."+str(gbk_record.annotations.get('sequence_version')),
                "version2" : str(gbk_record.name)+"."+str(gbk_record.annotations.get('sequence_version')),
                "keywords" : gbk_record.annotations.get('keywords'),
                "source" : gbk_record.annotations.get('source'),
                "organism" : gbk_record.annotations.get('organism'),
                "taxonomy" : gbk_record.annotations.get('taxonomy'),
                "author" : authors,
                "author1": auth1,
                "author2": auth2,
                "author3": auth3,
                "author4": auth4,
                "title": title,
                "title1": title1,
                "title2": title2,
                "title3": title3,
                "title4": title4,
                "journal" : journal,
                "journal1": jour1,
                "journal2": jour2,
                "journal3": jour3,
                "journal4": jour4,
                "structured_comment" : gbk_record.annotations.get('structured_comment'),
                "sequencing_technology" : csearch(gbk_record, "Sequencing Technology"),
                "assembly_method" : csearch(gbk_record, "Assembly Method"),
                "assembly_name" : csearch(gbk_record, "Assembly Name"),
                "qualifiersFeatures" : gbk_record.features[0].qualifiers,
                "taxonID" : f.fsearch(gbk_record, 'db_xref'),
                "location" : f.fsearch(gbk_record, 'geo_loc_name'),
                "geolocation" : f.fsearch(gbk_record, 'lat_lon'),
                "voucher" : f.fsearch(gbk_record, 'specimen_voucher'),
                "notes" :f.fsearch(gbk_record, 'note'),
                "organismFeatures" : f.fsearch(gbk_record, 'organism'),
                "organelle" : f.fsearch(gbk_record, 'organelle'),
                "moltypeFeatures" : f.fsearch(gbk_record, 'mol_type'),
                "cultivar" : f.fsearch(gbk_record, 'cultivar'),
                "tissue_type" : f.fsearch(gbk_record, 'tissue_type'),
                "collection_date" : f.fsearch(gbk_record, 'collection_date'),
                "collected_by" : f.fsearch(gbk_record, 'collected_by'),
                "identified_by" : f.fsearch(gbk_record, 'identified_by'),
                "PCR_primers" : f.fsearch(gbk_record, "PCR_primers"),
                "isolate" : f.fsearch(gbk_record, "isolate"),
                "isolate_source" : f.fsearch(gbk_record, "isolate_source"),
                "dev_stage" : f.fsearch(gbk_record, "dev_stage"),
                "clone" : f.fsearch(gbk_record, "clone"),
                "haplotype" : f.fsearch(gbk_record, "haplotype"),
                "bio_material" : f.fsearch(gbk_record, "bio_material"),
                "clone-lib": f.fsearch(gbk_record, "clone-lib"),
                "chromosome": f.fsearch(gbk_record, "chromosome"),
                "map": f.fsearch(gbk_record, "map"),
                "altitude": f.fsearch(gbk_record, "altitude"),
                "biotype": f.fsearch(gbk_record, "biotype"),
                "breed": f.fsearch(gbk_record, "breed"),
                "cell_type": f.fsearch(gbk_record, "cell_type"),
                "chemovar": f.fsearch(gbk_record, "chemovar"),
                "biovar": f.fsearch(gbk_record, "biovar"),
                "country": f.fsearch(gbk_record, "country"),
                "ecotype": f.fsearch(gbk_record, "ecotype"),
                "genotype": f.fsearch(gbk_record, "genotype"),
                "haplogroup": f.fsearch(gbk_record, "haplogroup"),
                "sub-species": f.fsearch(gbk_record, "sub-species"),
                "synonym": f.fsearch(gbk_record, "synonym"),
                "transgenic": f.fsearch(gbk_record, "transgenic"),
                "type": f.fsearch(gbk_record, "type"),
                "variety": f.fsearch(gbk_record, "variety"),
                "sequence" : gbk_record.seq
            }
            data.append(info)
        print("\n______________________________//______________________________\n\nData successfully parsed!")
    except FileNotFoundError:
        print("File was not found")
    except Exception as e:
        print(f"\n______________________________//______________________________\n\nFailed to parse genebank file: {e}\n")
    return data

# function to write in csv
def csv_write(data, output_file):
    # clause: if input file is empty
    if not data:
        print("No data to write.")
        return

    csv_header = [
        "id", "name", "length", "locus", "mol_type", "topology", "data_file_div", "date", "description", "definition",
        "accession", "version1", "version2", "keywords", "source", "organism", "taxonomy", "author", "author1", "author2",
        "author3", "author4", "title", "title1", "title2", "title3", "title4", "journal", "journal1", "journal2", "journal3",
        "journal4", "structured_comment", "sequencing_technology", "assembly_method", "assembly_name", "qualifiersFeatures",
        "taxonID", "location", "geolocation", "voucher", "notes", "organismFeatures", "organelle", "moltypeFeatures",
        "cultivar", "tissue_type", "collection_date", "collected_by", "identified_by", "isolate_source", "isolate",
        "PCR_primers", "dev_stage", "clone", "haplotype", "bio_material", "clone-lib", "chromosome", "map", "altitude",
        "biotype", "breed", "cell_type", "chemovar", "biovar", "country", "ecotype", "genotype", "haplogroup", "sub-species",
        "synonym", "transgenic", "type", "variety", "sequence"
    ]

    # attempts to write data in csv format
    try:
        with open(output_file, mode= "w", newline= "") as csvfile:
            ink = csv.DictWriter(csvfile, fieldnames= csv_header)
            ink.writeheader()
            for entry in data:
                ink.writerow(entry)
        print("\n______________________________//______________________________\n\nData successfully written to csv format!")
    # clause: something goes wrong with writing to csv
    except Exception as e:
        print(f"\n______________________________//______________________________\n\nFailed to write to CSV: {e}")


if __name__ == '__main__':
    main()
