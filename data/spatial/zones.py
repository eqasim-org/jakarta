import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.neighbors import KDTree

def configure(context, require):
    pass

def execute(context):
    df_zones = gpd.read_file("%s/spatial/JUTPI_Topologi_Check_Edited1.shp" % context.config["raw_data_path"])
    df_zones.crs = {"init" : "EPSG:4326"}
    df_zones = df_zones[["JUTPI_2009", "geometry"]]
    df_zones.columns = ["zone_id", "geometry"]
    

    #print(df_zones.count)
    #exit()



### delete zone which in the codes zone

    #df_codes = pd.read_csv("%s/spatial/codes.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')

    #df_zones['exist1'] = df_zones['zone_id'].isin(df_codes['id_zone'])
    #df_zones = df_zones[df_zones['exist1']==True]


    

    df_zones = df_zones.to_crs({"init" : "EPSG:5330"})

    #print(df_zones.count)
    #exit()

    return df_zones
