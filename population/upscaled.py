import pandas as pd
import numpy as np

def configure(context, require):
    require.stage("data.census.cleaned")

def execute(context):
    df_persons = context.stage("data.census.cleaned")
    df_persons = df_persons.sort_values(by = "person_id")

    #print("# Initial persons: %d" % len(df_persons))

    # Multiply persons
    #df_persons["multiplicator"] = np.round(df_persons["weight"]).astype(np.int)
    #df_persons = df_persons.iloc[np.repeat(np.arange(len(df_persons)), df_persons["multiplicator"])]
    #df_persons.loc[:, "new_person_id"] = np.arange(len(df_persons))
    #del df_persons["multiplicator"]

    # Clean up data frames
    #df_persons["census_person_id"] = df_persons["person_id"]
    #df_persons["person_id"] = df_persons["new_person_id"]
    #del df_persons["new_person_id"]

    #print("# Upscaled persons: %d" % len(df_persons))

    if "input_downsampling" in context.config:
        probability = context.config["input_downsampling"]

        person_ids = np.unique(df_persons["person_id"])
        f = np.random.random(size = (len(person_ids),)) < probability

        remaining_person_ids = person_ids[f]

        df_persons = df_persons[df_persons["person_id"].isin(remaining_person_ids)]
        print("# Downsampled persons: %d" % len(df_persons))

    #print(df_persons.count)
    #exit()
    return df_persons
