#! /usr/bin/env python3
import mgrs
import pandas as pd

def main():
    input = "test.csv"      # path to csv file to modify
    # preset functions
    normalize_dataframe(input, "normalized.csv")
    #clean_dataframe(input, "clean.csv")

    # functions can be chained together for a custom objective
    #df_to_csv(column_cleaner(row_cleaner(field_renamer(convert_coordinates("dirty.csv")))), "clean.csv")


# normalization function for coordinate datasets in MGRS format
def normalize_dataframe(input):         # add output csv paramater if running stand-alone
    # open csv file and read data as a dataframe
    df = pd.read_csv(input)

    df = coord_converter(df)             # convert mgrs to latlon
    df = field_renamer(df)               # renames respective fields to species(label), lat and lon
    df = row_cleaner(df)                 # deletes invalid rows
    df = column_cleaner(df)              # deletes extra columns
    #df_to_csv(df, output)               # write to csv (if needed)
    return df

# normalization function for latlon coordinate datasets
def clean_dataframe(input):             # add output csv paramater if running stand-alone
    # open csv file and read data as a dataframe
    df = pd.read_csv(input)
    # cleans dataset to include only label, lat and lon
    df = field_renamer(df)               # renames respective fields to species(label), lat and lon
    df = row_cleaner(df)                 # deletes invalid rows
    df = column_cleaner(df)              # deletes extra columns
    #df_to_csv(df, output)               # write to csv (if needed)
    return df


def mgrs_to_lat_lon(mgrs_coord):
    # create an MGRS object
    m = mgrs.MGRS()

    # convert MGRS to latitude and longitude
    lat_lon = m.toLatLon(mgrs_coord)

    return lat_lon


def coord_converter(df):
    # converts coordinates
    try:
        # call out coordinate conversion function to output to new dataframe columns "lat" and "lon"
        df[["lat", "lon"]] = df.iloc[:, 1].apply(mgrs_to_lat_lon).apply(pd.Series)     # df.iloc[:, 1] is specifying the column with MGRS coordinates. Ergo 1 because python is 0 sensitive

    except Exception as e:
        # exception clause
        print(f"Error converting MGRS coordinates: {e}")

    return df


def field_renamer(df):
    # renames important column for convention
    df.columns = [col if col not in ["taxon", "Taxon", "Species"] else "species" for col in df.columns]                 # add more name clause if needed
    df.columns = [col if col not in ["decimalLatitude", "Latitude", "latitude"] else "lat" for col in df.columns]       # add more name clause if needed
    df.columns = [col if col not in ["decimalLongitude", "Longitude", "longitude"] else "lon" for col in df.columns]    # add more name clause if needed

    return df


def row_cleaner(df):
    # conditional row deletion (taxonomic rank and null values)
    if "taxonRank" in df.columns:
        df = df[df["taxonRank"].isin(["SPECIES", "SUBSPECIES", "VARIETY"])]
    df = df[df["species"].notnull()]    # switch to notna() if needed
    df = df[df["lat"].notnull()]        # switch to notna() if needed
    df = df[df["lon"].notnull()]        # switch to notna() if needed

    return df


def column_cleaner(df):
    # deletes all fields/columns that are not label, lat and lon
    columns = [col for col in ["species", "lat", "lon"] if col in df.columns]
    df = df[columns]
    return df


def df_to_csv(df, output):
    # writes dataframe to csv
    try:
        df.to_csv(output, index=False)
        print(f"✅ Results written to {output}")

    except Exception as e:
        print(f"Error writing coordinates to csv: {e}")


# import protection
if __name__ == "__main__":
    main()
