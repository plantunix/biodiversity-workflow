#! /usr/bin/env python3
import os

from dotenv import find_dotenv, load_dotenv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from utils import clean_coords as cc


### SETTING UP ENVIRONMENT VARIABLES ###
# find .env automatically by cycling upstream directories until found
dotenv_path = find_dotenv()
# load entries as environment variables
load_dotenv(dotenv_path)
# define the environment variables
PORTUGAL = os.getenv("PORTUGAL")
ESPANHA = os.getenv("ESPANHA")
IBERIAN_BIOGEOGRAPHY = os.getenv("IBERIAN_BIOGEOGRAPHY")


# load territorial divisions (e.g. countries, provinces, biogeographic regions)
pt = gpd.read_file(PORTUGAL).to_crs("EPSG:4326")
es = gpd.read_file(ESPANHA).to_crs("EPSG:4326")
biogeo = gpd.read_file(IBERIAN_BIOGEOGRAPHY).to_crs("EPSG:4326")

# load occurrence data as GeoDataFrame
input = "test.csv"                    # raw occurrence dataset file
occ = cc.normalize_dataframe(input)    # normalizing occurrence datasets for further processing (MGRS)
#occ2 = cc.clean_dataframe(input2)      # normalizing occurrence datasets that dont need coord conversion (latlon)
gdf_occ = gpd.GeoDataFrame(
    occ, geometry=gpd.points_from_xy(occ.lon, occ.lat), crs="EPSG:4326"
)

# performs spatial join to assign each occurrence to a region
gdf_match = gpd.sjoin(gdf_occ, biogeo, how="left", predicate="within")


# aggregate regions by species
biogeography= (
    gdf_match.groupby("species")["code"]
    .apply(lambda x: ','.join(set(str(region) for region in x if
    pd.notna(region)))
    ).reset_index()
)
biogeography.columns = ["species", "biogeography"]


def gdf_to_csv(gdf, output):
    # writes geodataframe to csv
    try:
        gdf.to_csv(output, index=False)
        print(f"✅ Results written to {output}")

    except Exception as e:
        print(f"Error writing dataframe to csv: {e}")
#gdf_to_csv(biogeography, "biogeography.csv")    # aaand voilá


print(biogeography.head(10))

#########################################################################################################

def visualize(species):
# Visualization function:
    species_area = biogeo[
        biogeo["code"].isin(
            biogeography[biogeography["species"] == f"{species}"][
                "code"
            ]
        )
    ]       # This can then be plotted using .plot():

    species_area.plot(color='red')
    plt.show()

    # Or exported
    species_area.to_file(f"{species}_distribution.shp")


def geopandas_testing():
    gdf = pt
    print(len(gdf))
    print(gdf.crs)  # EPSG:4326
    print(gdf.geom_type)

    fig, ax = plt.subplots(1, figsize=(4.5, 10))
    gdf.plot("NAME_1", legend=True, legend_kwds={"loc": "center left"})
    leg = ax.get_legend()
    # leg.set_bbox_to_anchor((1.05, 0.5))
    plt.show()
