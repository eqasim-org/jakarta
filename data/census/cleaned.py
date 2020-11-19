from tqdm import tqdm
import pandas as pd
import numpy as np

def configure(context, require):
    pass

def execute(context):
    df = pd.read_csv("%s/census/census_full2.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')

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

    #Employment
    df.loc[df["socialStatus"] == "employed", "employment"] = "yes"
    df.loc[df["socialStatus"] == "student", "employment"] = "student"
    df.loc[df["socialStatus"] == "other", "employment"] = "no"
    df.loc[df["socialStatus"] == "housewife", "employment"] = "no"
    df.loc[df["socialStatus"] == "unemployed", "employment"] = "no"
    df.loc[df["socialStatus"] == "retired", "employment"] = "no"
    df["employment"] = df["employment"].astype("category")
    






    #df.loc[df["employed"] == 1, "employment"] = "yes"
    #df.loc[df["employed"] == 0, "employment"] = "no"
    #df.loc[(df["age"] < 18) & (df["age"] > 6), "student"] = 1
    #df.loc[df["student"] == 1, "employment"] = "student"
    #df.loc[(df["age"] < 6) | (df["age"] > 60), "employment"] = "no"
    #df.loc[df["age"] < 6, "employment"] = "no"
    #df["employment"] = df["employment"].astype("category")
    #df.loc[df["age"] < 6, "employment"] = "no"

    
    #df["age"] = df["age"].astype(np.int)
    #df["binary_car_availability"] = df["carAvailability"] == 1
    #df["income"] = np.round(df["householdIncome"] / df["numberOfMembers"])
    #df["income"] = df["totalIncome"]
    df["binary_mc_availability"] = df["mcAvailable"] > 0
    df["binary_vehicleAvailable"] = df["vehicleAvailable"] > 0
    
    df["binary_car_availability"] = (df["binary_vehicleAvailable"] == 1) | (df["binary_mc_availability"] == 1)

    df["binary_employed"] = df["employed"] > 0
    df["binary_student"] = df["student"] > 0
    
    #print(df.groupby('employment').count())
    #exit()

    # Clean up
    #df = df[[
     #   "person_id", "weight", "income",
     #   "zone_id", "age", "sex", "employment", "binary_car_availability"
    #]]

    #df.loc[df["hhIncome"] == 0.0, "hhIncome"] = 500.0
    #df.loc[df["hhIncome"] == 99.0, "hhIncome"] = 500.0    
    df.loc[df["hhIncome"] == 1.0, "hhIncome"] = 500.0
    df.loc[df["hhIncome"] == 2.0, "hhIncome"] = 2000.0
    df.loc[df["hhIncome"] == 3.0, "hhIncome"] = 4000.0
    df.loc[df["hhIncome"] == 4.0, "hhIncome"] = 6500.0
    df.loc[df["hhIncome"] == 5.0, "hhIncome"] = 10000.0
    df.loc[df["hhIncome"] == 6.0, "hhIncome"] = 13500.0
    df.loc[df["hhIncome"] == 7.0, "hhIncome"] = 16500.0
    df.loc[df["hhIncome"] == 8.0, "hhIncome"] = 19500.0
    df.loc[df["hhIncome"] == 9.0, "hhIncome"] = 22000.0
    df.loc[df["hhIncome"] == 10.0, "hhIncome"] = 24000.0
    df.loc[df["hhIncome"] == 11.0, "hhIncome"] = 30000.0
    #df.loc[df["hhIncome"] == 12.0, "hhIncome"] = 16500.0
    #df.loc[df["hhIncome"] == 13.0, "hhIncome"] = 18500.0
    #df.loc[df["hhIncome"] == 14.0, "hhIncome"] = 21500.0
    #df.loc[df["hhIncome"] == 15.0, "hhIncome"] = 23500.0
    #df.loc[df["hhIncome"] == 16.0, "hhIncome"] = 30000.0 
  





    df = df[[
        "person_id", "geo", "household_id","census_person_id",
        "age", "sex", "socialStatus", "hhIncome","binary_employed", "binary_student", "binary_mc_availability",
        "binary_car_availability", "employment", "employed"
    ]]


    #print(df['hhIncome'].value_counts())

    #print(df.hhIncome.count)
    #exit()
    #print(df.groupby('employment').count())
    #exit()


    

    return df
