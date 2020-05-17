import gzip
from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import numpy.linalg as la
import data.spatial.utils
import geopandas as gpd


def configure(context, require):
    require.stage("data.spatial.zones")
    require.stage("data.Opportunities.extract_roads_osm")


def execute(context):
    df_combined = pd.read_csv("%s/facilities_combined_25032020.csv" % context.config["raw_data_path"])
    df_combined = df_combined[["long", "lat", "tag"]]
    df_combined.columns = ["x", "y", "purpose"]
    #df = df[df["purpose"] == "shop"]    
    del df_combined["purpose"]
    df_opportunities = df_combined

    df_osm = pd.read_csv("%s/facilities_osm.csv" % context.config["raw_data_path"])
    df_osm = df_osm[["long", "lat", "tag"]]
    df_osm.columns = ["x", "y", "purpose"]
    #df = df[df["purpose"] == "shop"]    
    del df_osm["purpose"]
    df_osm = df_osm


    

    df_residential_road = context.stage("data.Opportunities.extract_roads_osm")[[
    "x", "y"]]
    
    #df_osm = data.spatial.utils.to_gpd(df_osm, crs = {"init" : "epsg:4326"})
    df_opportunities = pd.concat([df_opportunities, df_residential_road, df_osm])
    
    #from pyproj import Transformer

    #transformer = Transformer.from_crs('epsg:4326','epsg:5330',always_xy=True)
    #points = list(zip(df_osm.x,df_osm.y))
    #df_osm = np.array(list(transformer.itransform(points)))
    #df_zones = gpd.read_file(df_osm)
    #df_osm.crs = {"init" : "EPSG:4326"}
    #df_osm = df_osm.to_crs({"init" : "EPSG:5330"}

   
        
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

    df_opportunities = data.spatial.utils.to_gpd(df_opportunities, crs = {"init" : "EPSG:4326"})
    
    #print(df_opportunities.count)
    #exit()

    df_opportunities = data.spatial.utils.impute(df_opportunities, df_zones, "location_id", "zone_id", fix_by_distance = False).dropna()

    
    return df_opportunities
