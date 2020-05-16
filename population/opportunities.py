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
    df = pd.read_csv("%s/facilities_new.csv" % context.config["raw_data_path"])
    df.columns = ["x", "y", "purpose"]
    #df = df[df["purpose"] == "shop"]    
    del df["purpose"]

    df_opportunities = df

        
    #df_opportunities = pd.DataFrame(context.stage("data.bpe.cleaned")[[
    #    "bpe_id", "x", "y", "activity_type", "commune_id"
    #]], copy = True)
    #df_opportunities.columns = ["location_id", "x", "y", "activity_type", "commune_id"]

    df_opportunities["offers_work"] = True
    df_opportunities["offers_other"] = True

    df_opportunities["offers_leisure"] = True #df_opportunities["activity_type"] == "leisure"
    df_opportunities["offers_shop"] = True #df_opportunities["activity_type"] == "shop"
    df_opportunities["offers_education"] = True #df_opportunities["activity_type"] == "education"

    df_opportunities["offers_home"] = True

    df_opportunities["location_id"] = np.arange(len(df_opportunities))

    #df_zones = context.stage("data.spatial.zones")[["zone_id", "commune_id", "zone_level"]]
    #df_zones = df_zones[df_zones["zone_level"] == "commune"][["zone_id", "commune_id"]]
    #df_opportunities = pd.merge(df_opportunities, df_zones, on = "commune_id")

    df_zones = context.stage("data.spatial.zones")
    #print(df_zones.count)
    #exit()

    df_opportunities = data.spatial.utils.to_gpd(df_opportunities, crs = {"init" : "EPSG:5330"})
    df_opportunities = data.spatial.utils.impute(df_opportunities, df_zones, "location_id", "zone_id", fix_by_distance = False).dropna()

    
    return df_opportunities
