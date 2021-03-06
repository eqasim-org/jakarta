import gzip
from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import numpy.linalg as la
import os
import eqasim.location_assignment as eqla

def configure(context, require):
    require.stage("population.trips")
    require.stage("data.hts.cleaned")
    require.stage("matsim.java.eqasim")
    require.stage("utils.java")
    require.stage("matsim.population")
    require.stage("matsim.facilities")

def execute(context):
    threads = context.config["threads"]
    primary_activities = ["home", "work", "education"]

    df_persons = context.stage("data.hts.cleaned")[0][["person_id", "weight"]]
    df_trips = context.stage("data.hts.cleaned")[1][["person_id", "trip_id", "mode", "crowfly_distance", "departure_time", "arrival_time", "purpose"]]
    df_trips = pd.merge(df_trips, df_persons[["person_id", "weight"]], on = "person_id")

    df_trips["travel_time"] = df_trips["arrival_time"] - df_trips["departure_time"]
    df_trips = df_trips[df_trips["travel_time"] > 0.0]
    df_trips = df_trips[df_trips["crowfly_distance"] > 0.0]

    df_trips["following_purpose"] = df_trips["purpose"]
    df_trips["preceeding_purpose"] = df_trips["purpose"].shift(1)
    df_trips.loc[df_trips["trip_id"] == 1, "preceeding_purpose"] = "home"

    df_trips = df_trips[~(
        df_trips["preceeding_purpose"].isin(primary_activities) &
        df_trips["following_purpose"].isin(primary_activities)
    )]

    df_trips = df_trips.rename(columns = {
        "crowfly_distance": "distance"
    })[["mode", "travel_time", "distance", "weight"]]
    

    	
    #print(df_trips[df_trips["mode"]=='bike'])
    #print(df_trips[df_trips["mode"]=='pt'])
    df_trips = df_trips.astype({'travel_time': 'float64'})
    df_trips = df_trips.astype({'weight': 'float64'})
    print(df_trips.dtypes)
    eqla.create_input_distributions(
        df_trips, context.cache_path, bin_size=10, #it was 50
        #modes = ["car","motorcycle", "walk", "pt","car_passenger", "carodt", "mcodt"],
        #resampling_factors = {
        #    "car": 0.9, "walk": 0.0, "pt": 0.2, "motorcycle" : 0.9, "car_passenger" : 0.3, "carodt" : 0.3, "mcodt" : 0.3
        #}
    )
    
    #print(df_trips.count)
    #exit()

    quantiles_path = "%s/quantiles.dat" % context.cache_path
    distributions_path = "%s/distributions.dat" % context.cache_path

    java = context.stage("utils.java")
    input_population_path = context.stage("matsim.population")
    input_facilities_path = context.stage("matsim.facilities")
    output_population_path = "%s/population_with_locations.xml.gz" % context.cache_path
    output_statistics_path = "none" # "%s/statistics.csv" % context.cache_path <- DISABLED!

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.core.scenario.location_assignment.RunLocationAssignment", [
        "--population-path", input_population_path,
        "--facilities-path", input_facilities_path,
        "--quantiles-path", quantiles_path,
        "--distributions-path", distributions_path,
        "--output-path", output_population_path,
        "--threads", str(context.config["threads"]),
        "--random-seed", str(0)
    ],cwd = context.cache_path)

    assert(os.path.exists(output_population_path))

    # Now, impute innerParis attribute

    #input_population_path = output_population_path
    #output_population_path = "%s/population_with_inner_paris.xml.gz" % context.cache_path
    #iris_path = "%s/inner_paris_iris.shp" % context.cache_path

    #df_iris = context.stage("data.spatial.iris")
    #df_iris = df_iris[df_iris["iris_id"].str.startswith("75")]
    #df_iris.to_file(iris_path)

    #java(
    #    context.stage("matsim.java.baseline"), "ch.ethz.matsim.baseline_scenario.paris.ImputeInnerParisAttribute", [
    #        "--iris-path", iris_path,
    #        "--input-path", input_population_path,
    #        "--output-path", output_population_path
    #    ], cwd = context.cache_path)

    assert(os.path.exists(output_population_path))
    return output_population_path
