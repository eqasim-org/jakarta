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
    #df_combined = pd.read_csv("%s/facilities_combined_25032020.csv" % context.config["raw_data_path"])
    #df_combined = df_combined[["long", "lat", "tag"]]
    #df_combined.columns = ["x", "y", "purpose"]
    #df = df[df["purpose"] == "shop"]    
    #del df_combined["purpose"]
    #df_opportunities = df_combined

    #df_osm = pd.read_csv("%s/facilities_osm.csv" % context.config["raw_data_path"])
    #df_osm = df_osm[["long", "lat", "tag"]]
    #df_osm.columns = ["x", "y", "purpose"]
    #df = df[df["purpose"] == "shop"]    
    #del df_osm["purpose"]
    #df_osm = df_osm


    

    df_residential_road = context.stage("data.Opportunities.extract_roads_osm")[[
    "x", "y"]]
    
    #df_osm = data.spatial.utils.to_gpd(df_osm, crs = {"init" : "epsg:4326"})
    df_opportunities = df_residential_road.copy()
    
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
    df_opportunities["offers_leisure"] = True
    df_opportunities["offers_shop"] = True
    df_opportunities["offers_education"] = True
    df_opportunities["offers_home"] = True

    df_zones = context.stage("data.spatial.zones")
    zone_ids = set(np.unique(df_zones["zone_id"]))
    df_opportunities["location_id"] = np.arange(len(df_opportunities))

    df_opportunities = data.spatial.utils.to_gpd(df_opportunities, crs = {"init" : "EPSG:4326"})
    df_opportunities = data.spatial.utils.impute(df_opportunities, df_zones, "location_id", "zone_id", fix_by_distance = False).dropna()

    existing_zone_ids = set(np.unique(df_opportunities["zone_id"]))
    missing_zone_ids = zone_ids - existing_zone_ids    
        
    #assign locations to centroids only for the missing zone ids
    df_centroids = df_zones[df_zones["zone_id"].isin(missing_zone_ids)].copy()
    df_centroids["x"] = df_centroids["geometry"].centroid.x
    df_centroids["y"] = df_centroids["geometry"].centroid.y
    df_centroids["offers_work"] = True
    df_centroids["offers_education"] = True
    df_centroids["offers_other"] = True
    df_centroids["offers_leisure"] = True
    df_centroids["offers_shop"] = True
    df_centroids["offers_home"] = True 

    

    df_opportunities = pd.concat([df_opportunities, df_centroids], sort = True)
    df_opportunities["location_id"] = np.arange(len(df_opportunities))


    

    print(df_opportunities.columns)
    exit()
     
    return df_opportunities
