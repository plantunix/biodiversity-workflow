#! /usr/bin/env python3
import os

from dotenv import find_dotenv, load_dotenv

import geobio as biog
from functions import get_conservation_status as iucn

### SETTING UP ENVIRONMENT VARIABLES ###
# find .env automatically by cycling upstream directories until found
dotenv_path = find_dotenv()
# load entries as environment variables
load_dotenv(dotenv_path)
# define the environment variables
# USERNAME = os.getenv("USERNAME")
# PASSWORD = os.getenv("PASSWORD")


def main():
    checklist = ["Quercus suber", "Quercus faginea"]

    cstatus = iucn(checklist)

    print(cstatus)


if __name__ == "__main__":
   main()
