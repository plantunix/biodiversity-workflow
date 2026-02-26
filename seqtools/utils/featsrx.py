## feature search function ##
def fsearch(record, key):                                                        # Features are lists() within a record, each
    features = record.features                                                   # item (feature) has a dict() named qualifiers,
    keys = [                                                                     # which has multiple different key-values pairs
        "db_xref", "geo_loc_name", "specimen_voucher", "note", "organism",       # depending on the metadata the publisher made
        "organelle", "mol_type", "cultivar", "tissue_type", "collection_date",   # public and how he/she organized record structure.
        "collected_by","identified_by","PCR_primers","isolate","isolate_source", # This function will take on predefined qualifier
        "dev_stage","clone","haplotype","bio_material","clone-lib", "chromosome",# keys as parameters and search feature.qualifier[]
        "map", "altitude", "biotype", "breed", "cell_type", "chemovar", "biovar",# structure and return its value.
        "lat_lon", "country", "ecotype", "genotype", "haplogroup", "sub-species",
        "synonym", "transgenic", "type", "variety"
    ]
    for feature in features:
        if key in keys:
            if key in feature.qualifiers:
                value = feature.qualifiers[key][0]
            else:
                value = 'Not Available'
            return value
        else:
            error = f"Invalid function parameter '{key}'. Feature search function accepts only db_xref, geo_loc_name, specimen_voucher,\
            note, organism, organelle, mol_type, cultivar, tissue_type, collection_date or collected_by, identified_by, PCR_primers,\
            isolate, isolate_source, dev_stage, clone, haplotype, bio_material, clone-lib, chromosome, map, altitude, biotype, breed,\
            cell_type, chemovar, biovar, lat_lon, country, ecotype, genotype, haplogroup, sub-species, synonym, transgenic, type or\
            variety as parameters."
            print(error)
            return
