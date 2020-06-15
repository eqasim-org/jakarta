import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

def configure(context, require):
    #require.stage("matsim.population")
    require.stage("population.sociodemographics")
    require.stage("population.activities")
    require.stage("population.trips")
    require.stage("population.spatial.locations")

    


def execute(context):
    #df_populations = context.stage("matsim.population")
    df_persons = context.stage("population.sociodemographics")
    df_activities = context.stage("population.activities")

    # Attach following modes to activities
    df_trips = pd.DataFrame(context.stage("population.trips"), copy = True)[["person_id", "trip_id", "mode"]]
    df_trips.columns = ["person_id", "activity_id", "following_mode"]
    df_activities = pd.merge(df_activities, df_trips, on = ["person_id", "activity_id"], how = "left")

    # Attach locations to activities
    df_locations = context.stage("population.spatial.locations")
    df_activities = pd.merge(df_activities, df_locations, on = ["person_id", "activity_id"], how = "left")

    # Bring in correct order (although it should already be)
    df_persons = df_persons.sort_values(by = "person_id")
    df_activities = df_activities.sort_values(by = ["person_id", "activity_id"])

    exclude =  df_activities.person_id.isin(df_locations.person_id)
    df_activities = df_activities[exclude]


    print(df_activities.count)
    exit()