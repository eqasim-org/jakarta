import gzip
from tqdm import tqdm
import pandas as pd
import numpy as np
#import data.constants as c
import shapely.geometry as geo
import multiprocessing as mp

def configure(context, require):
    require.stage("data.od.cleaned")
    require.stage("data.spatial.zones")
    require.stage("population.sociodemographics")
    require.stage("population.trips")

# TODO: There are some points for improvement:
# - 2. We can add a second step where an IRIS is sampled for each person (given
#      the commune). First this could be done by distance, or by number of enterprises
#      in the IRIS. We can get this information from BPE.
# - 3. Unfortunately we only have a work place density, not a density of employment. If
#      we would find this somehwere, it would be even better!
# - 4. We can parallelize this stage easily!

def execute(context):
    df_persons = pd.DataFrame(context.stage("population.sociodemographics")[["person_id", "zone_id", "hts_person_id", "has_work_trip", "has_education_trip"]], copy = True)
    df_persons = df_persons

       

    df_trips = context.stage("population.trips")[["person_id", "following_purpose"]]
    df_work_od, df_education_od = context.stage("data.od.cleaned")

    #print(df_work_od.count)
    #exit()

 
    
    df_home = df_persons[["person_id", "zone_id"]]
    #df_home.columns = ["hts_person_id", "zone_id"]

   

    # First, home zones
    #print("Attaching home zones ...")
    #df_households = df_persons #.drop_duplicates("household_id")
    #df_households = pd.merge(df_households, df_home, on = "hts_person_id", how = "left")
    #assert(not df_households["hts_person_id"].isna().any())
    #df_home = df_households[["household_id", "zone_id"]]

    #df_persons = pd.merge(df_persons, df_households[["household_id", "zone_id"]], on = "household_id")

    # Second, work zones
    df_work = []

    

    for origin_id in tqdm(np.unique(df_persons["zone_id"]), desc = "Sampling work zones"):
        f = (df_persons["zone_id"] == origin_id) & df_persons["has_work_trip"]
        df_origin = pd.DataFrame(df_persons[f][["person_id"]], copy = True)
        df_destination = df_work_od[df_work_od["origin_id"] == origin_id]

        if len(df_origin) > 0:
            counts = np.random.multinomial(len(df_origin), df_destination["weight"].values)
            indices = np.repeat(np.arange(len(df_destination)), counts)
            df_origin.loc[:, "zone_id"] = df_destination.iloc[indices]["destination_id"].values
            df_work.append(df_origin[["person_id", "zone_id"]])

    df_work = pd.concat(df_work)

    # Third, education zones
    df_education = []

    for origin_id in tqdm(np.unique(df_persons["zone_id"]), desc = "Sampling education zones"):
        f = (df_persons["zone_id"] == origin_id) & df_persons["has_education_trip"]
        df_origin = pd.DataFrame(df_persons[f][["person_id"]], copy = True)
        df_destination = df_education_od[df_education_od["origin_id"] == origin_id]

        if len(df_origin) > 0:
            counts = np.random.multinomial(len(df_origin), df_destination["weight"].values)
            indices = np.repeat(np.arange(len(df_destination)), counts)
            df_origin.loc[:, "zone_id"] = df_destination.iloc[indices]["destination_id"].values
            df_education.append(df_origin[["person_id", "zone_id"]])

    df_education = pd.concat(df_education)

    # Impute zones
    #df_zones = context.stage("data.spatial.zones")
    #df_zones = df_zones[df_zones["zone_level"] == "commune"]

    #df_work = pd.merge(df_work, df_zones[["zone_id", "zone_id"]], on = "zone_id")
    #df_education = pd.merge(df_education, df_zones[["zone_id", "zone_id"]], on = "zone_id")

    #df_work = df_work[["person_id", "zone_id"]]
    #df_education = df_education[["person_id", "zone_id"]]

    return df_home, df_work, df_education
