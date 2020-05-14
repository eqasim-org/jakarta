import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.neighbors import KDTree

def configure(context, require):
    pass

def execute(context):
    df_zones = gpd.read_file("%s/spatial/JUTPI_Topologi_Check_Edited.shp" % context.config["raw_data_path"])
    df_zones.crs = {"init" : "EPSG:4326"}
    df_zones = df_zones[["ZONE_ID", "geometry"]]
    df_zones.columns = ["zone_id", "geometry"]
    #print(df_zones.columns)
    #exit()
    df_zones = df_zones.to_crs({"init" : "EPSG:5330"})
    return df_zones
