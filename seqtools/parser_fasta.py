#! /usr/bin/env python3
import time
import csv
from Bio import SeqIO

def main():
    # assign file path to parse here: e.g. relative "output.txt" or absolute "/home/user/Documents/output.txt"
    _input_file= "output.txt"
    _output_file = "fasta.csv"
    # actually running the alll them functionz
    previewFasta(_input_file)
    parsed_data = parseFasta(_input_file)
    csv_write(parsed_data, _output_file)

# preview function
def previewFasta(_input_file):
    # assign list of plant sequences for data parsing from fasta file
    # open the file
    with open(_input_file, "r") as file:
        # read all the lines (aka species seq) from the file
        data_list = list(SeqIO.parse(file, "fasta"))
    # preview of the quantity of records identified and small timer
    print("\nFound {} records!".format(len(data_list)))
    time.sleep(1)
    # preview of first and last sequences
    if data_list:
        for i, seq_record in enumerate(data_list):
            # a little embezzlement to take the ID out of the description string (which is assumed by default)
            descriptor = str(seq_record.description)
            description = descriptor[len(seq_record.id)+1:]
            # preview first sequence
            if i == 0:
                print("\nFirst Sequence Record -")
                print("ID:", seq_record.id, ";  Sequence length:", len(seq_record.seq), ";  Description:", description)
            # preview last sequence
            elif i == len(data_list)-1:
                print("\nLast Sequence Record -")
                print("ID:", seq_record.id, ";  Sequence length:", len(seq_record.seq), ";  Description:", description)
    # clause: something goes wrong with the preview
    else:
        print("No sequence data was found or failed to parse! :(")

# parsing function
def parseFasta(_input_file):
    # initialize list object to store useful data
    data = []
    try:
        # assign fasta entry data to dict() form for each sequence,
        # specifying the keys for each entry. Store each dict() as entry in data list()
        for seq_record in SeqIO.parse(_input_file, "fasta"):
            descriptor = str(seq_record.description)
            description = descriptor[len(seq_record.id) + 1:]
            info = {"id": seq_record.id, "description": description, "length": len(seq_record.seq), "sequence": seq_record.seq}
            data.append(info)
        print("\n______________________________//______________________________\n\nData successfully parsed!")
    except FileNotFoundError:
        print("File was not found")
    except Exception as e:
        print(f"\n______________________________//______________________________\n\nFailed to parse fasta file: {e}\n")
    return data

# function to write csv
def csv_write(data, _output_file):
    # clause: if input file is empty
    if not data:
        print("No data to write.")
        return

    csv_header = ["id","description", "length", "sequence"]
    # attempts to write data to csv format.
    try:
        with open(_output_file, mode= "w", newline="") as csvfile:
            ink = csv.DictWriter(csvfile, fieldnames=csv_header)
            ink.writeheader()
            for entry in data:
                ink.writerow(entry)
        print("\n______________________________//______________________________\n\nData successfully written to csv format!")   #{_output_file}
    # clause: something goes wrong with writing to csv
    except Exception as e:
        print(f"\n______________________________//______________________________\n\nFailed to write to CSV: {e}")

# import protection
if __name__ == "__main__":
    main()
