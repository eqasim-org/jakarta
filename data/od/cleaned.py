from tqdm import tqdm
import pandas as pd
import numpy as np
import simpledbf
import itertools

def configure(context, require):
    require.stage("data.spatial.zones")

def fix_zones(df, df_mapping, source_column, target_column):
    df["__long_zone_id"] = df[source_column]
    df = pd.merge(df, df_mapping, how = "left", on = "__long_zone_id")
    del df["__long_zone_id"]
    df[target_column] = df["__short_zone_id"]
    del df["__short_zone_id"]
    return df

def execute(context):
    df_mapping = pd.read_csv("%s/spatial/codes.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')

    #print(df_mapping.columns)
    #exit()

    df_mapping.columns = ["observation", "zone_id", "__short_zone_id"]
    df_mapping = df_mapping[["zone_id", "__short_zone_id"]]



    df_work = pd.read_csv("%s/ODs/OD_work_update.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')
    df_work.columns = ["origin_id", "destination_id", "weight"]


   




    df_education = pd.read_csv("%s/ODs/OD_education_update.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')
    df_education.columns = ["origin_id", "destination_id", "weight"]

    #df_work = fix_zones(df_work, df_mapping, "long_origin_id", "origin_id")


    

    #df_work = fix_zones(df_work, df_mapping, "long_destination_id", "destination_id")
    #df_education = fix_zones(df_education, df_mapping, "long_origin_id", "origin_id")
    #df_education = fix_zones(df_education, df_mapping, "long_destination_id", "destination_id")

    #del df_work["long_origin_id"]
    #del df_work["long_destination_id"]
    #del df_education["long_origin_id"]
    #del df_education["long_destination_id"]

    zone_ids = set(np.unique(df_mapping["zone_id"]))
    #zone_ids |= set(np.unique(df_work["origin_id"]))
    #zone_ids |= set(np.unique(df_work["destination_id"]))
    #zone_ids |= set(np.unique(df_education["origin_id"]))
    #zone_ids |= set(np.unique(df_education["destination_id"]))

    # Compute totals
    df_work_totals = df_work[["origin_id", "weight"]].groupby("origin_id").sum().reset_index()
    df_work_totals["total"] = df_work_totals["weight"]
    del df_work_totals["weight"]

    df_education_totals = df_education[["origin_id", "weight"]].groupby("origin_id").sum().reset_index()
    df_education_totals["total"] = df_education_totals["weight"]
    del df_education_totals["weight"]

    # Impute totals
    #df_work = pd.merge(df_work, df_work_totals, on = ["origin_id", "commute_mode"])
    df_work = pd.merge(df_work, df_work_totals, on = "origin_id")
    df_education = pd.merge(df_education, df_education_totals, on = "origin_id")

    # Compute probabilities
    df_work["weight"] /= df_work["total"]
    df_education["weight"] /= df_education["total"]

    assert(sum(df_work_totals["total"] == 0.0) == 0)
    assert(sum(df_education_totals["total"] == 0.0) == 0)

    # Cleanup
    df_work = df_work[["origin_id", "destination_id", "weight"]]
    df_education = df_education[["origin_id", "destination_id", "weight"]]

    # Fix missing zones
    existing_work_ids = set(np.unique(df_work["origin_id"]))
    missing_work_ids = zone_ids - existing_work_ids
    existing_education_ids = set(np.unique(df_education["origin_id"]))
    missing_education_ids = zone_ids - existing_education_ids

    # TODO: Here we could take the zones of nearby zones in the future. Right now
    # we just distribute evenly (after all these zones don't seem to have a big impact
    # if there is nobody in the data set).

    work_rows = []
    for origin_id in missing_work_ids:
        for destination_id in existing_work_ids:
            work_rows.append((origin_id, destination_id, 1.0 / len(existing_work_ids)))
    df_work = pd.concat([df_work, pd.DataFrame.from_records(work_rows, columns = ["origin_id", "destination_id", "weight"])])

    education_rows = []
    for origin_id in missing_education_ids:
        for destination_id in existing_education_ids:
            education_rows.append((origin_id, destination_id, 1.0 / len(existing_education_ids)))
    df_education = pd.concat([df_education, pd.DataFrame.from_records(education_rows, columns = ["origin_id", "destination_id", "weight"])])

    # At the end we don't want to have a zone as a destination if it does not
    # contain a work or education facility. Hence, we set those destinations to
    # zero and reweight everything here. TODO: We could further integrate this
    # into the code above to streamline this.

    #df_bpe = context.stage("data.bpe.cleaned")[["zone_id", "activity_type"]]

    #df_counts = df_bpe.groupby("zone_id").size().reset_index(name = "count")
    #existing_zone_ids = set(np.unique(df_counts["zone_id"]))
    #missing_work_zone_ids = zone_ids - existing_zone_ids

    #df_counts = df_bpe[df_bpe["activity_type"] == "education"]
    #df_counts = df_counts.groupby("zone_id").size().reset_index(name = "count")
    #existing_zone_ids = set(np.unique(df_counts["zone_id"]))
    #missing_education_zone_ids = zone_ids - existing_zone_ids

    #print("Communes without work locations:", len(missing_work_zone_ids))
    #print("Communes without education locations:", len(missing_education_zone_ids))

    #df_work.loc[df_work["destination_id"].isin(missing_work_zone_ids), "weight"] = 0.0
    #df_education.loc[df_education["destination_id"].isin(missing_education_zone_ids), "weight"] = 0.0

    df_total = df_work[["origin_id", "weight"]].groupby("origin_id").sum().rename({"weight" : "total"}, axis = 1)
    df_work = pd.merge(df_work, df_total, on = "origin_id")
    df_work["weight"] /= df_work["total"]
    del df_work["total"]

    df_total = df_education[["origin_id", "weight"]].groupby("origin_id").sum().rename({"weight" : "total"}, axis = 1)
    df_education = pd.merge(df_education, df_total, on = "origin_id")
    df_education["weight"] /= df_education["total"]
    del df_education["total"]

    #print(df_education.columns)
    #exit()

    return df_work, df_education
