import gzip
from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import numpy.linalg as la
import data.spatial.utils

def configure(context, require):
    require.stage("data.spatial.zones")

def execute(context):
    df_opportunities = context.stage("data.opportunities.extract_roads_osm") 
    df_opportunities = df_opportunities[["x", "y"]]
    df_opportunities.columns = ["x", "y"]    
    
    df_opportunities["offers_work"] = True
    df_opportunities["offers_other"] = True
    df_opportunities["offers_leisure"] = True
    df_opportunities["offers_shop"] = True 
    df_opportunities["offers_education"] = False
    df_opportunities["offers_home"] = True
   
    df_zones = context.stage("data.spatial.zones")

    df_opportunities = data.spatial.utils.to_gpd(df_opportunities, crs = {"init" : "EPSG:4326"}).to_crs({"init" : "EPSG:5330"})
    df_opportunities["location_id"] = np.arange(len(df_opportunities))
    df_opportunities = data.spatial.utils.impute(df_opportunities, df_zones, "location_id", "zone_id", fix_by_distance = False).dropna()
    
    return df_opportunities
