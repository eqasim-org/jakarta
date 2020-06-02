from tqdm import tqdm
import pandas as pd
import numpy as np

def configure(context, require):
    pass

def execute(context):
    df = pd.read_csv("%s/census/census_full.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')

    #don't need it yet
    #del df["hasSalary"]
    #del df["salaryAMount"]

    # don't need it yet
    # These are only children!
    #df["totalIncome"] = df["totalIncome"].fillna(0.0)

    #assert(not np.any(df.isna()))

    # don't need it yet
    # Put person IDs
    df.loc[:, "person_id"] = df["unique_person_id"]
    df.loc[:, "household_id"] = df["unique_housing_id"]
    df.loc[:, "census_person_id"] = df["pid"]
    #df.loc[:, "weight"] = df["personWeight"]

    # Spatial
    #df["long_zone_id"] = df["areaCode"]

    #df_mapping = pd.read_csv("%s/Spatial/codes.csv" % context.config["raw_data_path"], sep = ";")
    #df_mapping.columns = ["observation", "long_zone_id", "zone_id"]
    #df_mapping = df_mapping[["long_zone_id", "zone_id"]]

    #df = pd.merge(df, df_mapping, how = "left", on = "long_zone_id")

    #f = df["zone_id"].isna()
    #print("Removing %d/%d (%.2f%%) persons from census (outside of area)" % (
    #    np.sum(f), len(df), 100.0 * np.sum(f) / len(df)
    #))
    #df = df[~f]
    #df["zone_id"] = df["zone_id"].astype(np.int)

    # Attributes
    df.loc[df["sex"] == 1, "sex"] = "male"
    df.loc[df["sex"] == 2, "sex"] = "female"
    df["sex"] = df["sex"].astype("category")

    #df["__employment"] = df["employment"]
    #df.loc[df["__employment"] == 1, "employment"] = "yes"
    #df.loc[df["__employment"] == 2, "employment"] = "no"
    #df.loc[df["__employment"] == 3, "employment"] = "student"
    #df["employment"] = df["employment"].astype("category")

    #df["age"] = df["age"].astype(np.int)
    #df["binary_car_availability"] = df["carAvailability"] == 1
    #df["income"] = np.round(df["householdIncome"] / df["numberOfMembers"])
    #df["income"] = df["totalIncome"]
    df["binary_mc_availability"] = df["mcAvailable"] > 0
    df["binary_car_availability"] = df["vehicleAvailable"] > 0
    df["binary_employed"] = df["employed"] > 0
    df["binary_student"] = df["student"] > 0


    # Clean up
    #df = df[[
     #   "person_id", "weight", "income",
     #   "zone_id", "age", "sex", "employment", "binary_car_availability"
    #]]

    df.loc[df["hhIncome"] == 0.0, "hhIncome"] = 500.0
    df.loc[df["hhIncome"] == 99.0, "hhIncome"] = 500.0    
    df.loc[df["hhIncome"] == 1.0, "hhIncome"] = 500.0
    df.loc[df["hhIncome"] == 2.0, "hhIncome"] = 1300.0
    df.loc[df["hhIncome"] == 3.0, "hhIncome"] = 1800.0
    df.loc[df["hhIncome"] == 4.0, "hhIncome"] = 2500.0
    df.loc[df["hhIncome"] == 5.0, "hhIncome"] = 3500.0
    df.loc[df["hhIncome"] == 6.0, "hhIncome"] = 4500.0
    df.loc[df["hhIncome"] == 7.0, "hhIncome"] = 5500.0
    df.loc[df["hhIncome"] == 8.0, "hhIncome"] = 7000.0
    df.loc[df["hhIncome"] == 9.0, "hhIncome"] = 9000.0
    df.loc[df["hhIncome"] == 10.0, "hhIncome"] = 11500.0
    df.loc[df["hhIncome"] == 11.0, "hhIncome"] = 13500.0
    df.loc[df["hhIncome"] == 12.0, "hhIncome"] = 16500.0
    df.loc[df["hhIncome"] == 13.0, "hhIncome"] = 18500.0
    df.loc[df["hhIncome"] == 14.0, "hhIncome"] = 21500.0
    df.loc[df["hhIncome"] == 15.0, "hhIncome"] = 23500.0
    df.loc[df["hhIncome"] == 16.0, "hhIncome"] = 30000.0 
  





    df = df[[
        "person_id", "geo", "household_id","census_person_id",
        "age", "sex", "socialStatus", "hhIncome","binary_employed", "binary_student", "binary_mc_availability",
        "binary_car_availability"
    ]]


    #print(df['hhIncome'].value_counts())

    #print(df.hhIncome.count)
    #exit()

    

    return df
