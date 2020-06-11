from tqdm import tqdm
import pandas as pd
import numpy as np

def configure(context, require):
    pass

def execute(context):
    df_persons = pd.read_csv("%s/HTS/header_persons_final_used2.csv" % context.config["raw_data_path"], sep = ",",  encoding= 'unicode_escape')
   
    df_codes = pd.read_csv("%s/spatial/codes.csv" % context.config["raw_data_path"], sep = ",", encoding= 'unicode_escape')

### delete individu which are not living in the zone

    #df_persons['exist1'] = df_persons['home_zone'].isin(df_codes['id_zone'])
    #df_persons = df_persons[df_persons['exist1']==True]

    #print(df_persons.count)
    #exit()

#I don't need this
    #for column in ["weight_trip", "number_of_bikes", "number_of_motorcycles", "weekday"]:
       # del df_persons[column]

    #print("Filling %d/%d observations with number_of_cars = 0" % (np.sum(df_persons["number_of_cars"].isna()), len(df_persons)))
    #df_persons["number_of_cars"] = df_persons["number_of_cars"].fillna(0.0)
    #df_persons["number_of_cars"] = df_persons["number_of_cars"].astype(np.int)

    #print("Removing %d/%d observations with NaN personal_income" % (np.sum(df_persons["personal_income"].isna()), len(df_persons)))
    #df_persons = df_persons[~df_persons["personal_income"].isna()]

    # ID and weight
    # I don't need this
    #df_persons.loc[:, "person_id"] = df_persons["observation"]
    #df_persons.loc[:, "weight"] = df_persons["weight_person"]

    # Attributes
    # I don't need this
    df_persons.loc[df_persons["sex"] == 1, "sex"] = "male"
    df_persons.loc[df_persons["sex"] == 2, "sex"] = "female"
    df_persons["sex"] = df_persons["sex"].astype("category")

    # I don't need this
    #df_persons["__employment"] = df_persons["employed"]
    #df_persons.loc[df_persons["__employment"] == 1, "employment"] = "yes"
    #df_persons.loc[df_persons["__employment"] == 2, "employment"] = "no"
    #df_persons.loc[df_persons["__employment"] == 3, "employment"] = "student"
    #df_persons["employment"] = df_persons["employment"].astype("category")

    #df_persons["age"] = df_persons["age"].astype(np.int)
    #df_persons["binary_car_availability"] = df_persons["number_of_cars"] > 0
    
    df_persons["binary_mc_availability"] = df_persons["number_of_motorcycles"] > 0
    df_persons["binary_car_availability"] = df_persons["number_of_cars"] > 0

    df_persons["binary_employed"] = df_persons["employed"] > 0
    df_persons["binary_student"] = df_persons["student"] > 0



    #df_persons["income"] = df_persons["personal_income"]

    # Clean up

    #df_persons = df_persons[[
        #"person_id", "weight",
        #"age", "sex", "employment", "binary_car_availability",
        #"income"
    #]]

    df_persons = df_persons[[
    "household_id", "person_id", "weight",
    "home_zone", "age", "sex",
    "binary_mc_availability", "binary_car_availability", "binary_employed","binary_student",
    "household_income"
     ]]
    
    #print(df_persons.count)
    #exit()
    # Trips

    df_trips = pd.read_csv("%s/HTS/header_trips_Jakarta_3.csv" % context.config["raw_data_path"], sep = ",",  encoding= 'unicode_escape')

    ### delete individu which are not living in the zone

    #df_trips['exist1'] = df_trips['person_id'].isin(df_persons['person_id'])
    #df_trips = df_trips[df_trips['exist1']==True]

    
    ### change trip purpose and mode



    df_trips.loc[df_trips["destination_purpose"] == 1, "destination_purpose"] = "home"
    df_trips.loc[df_trips["destination_purpose"] == 2, "destination_purpose"] = "other"
    df_trips.loc[df_trips["destination_purpose"] == 3, "destination_purpose"] = "work"
    df_trips.loc[df_trips["destination_purpose"] == 4, "destination_purpose"] = "education"
    df_trips.loc[df_trips["destination_purpose"] == 5, "destination_purpose"] = "shop"
    df_trips.loc[df_trips["destination_purpose"] == 6, "destination_purpose"] = "shop"
    df_trips.loc[df_trips["destination_purpose"] == 7, "destination_purpose"] = "leisure"
    df_trips.loc[df_trips["destination_purpose"] == 8, "destination_purpose"] = "other"
    df_trips.loc[df_trips["destination_purpose"] == 9, "destination_purpose"] = "leisure"
    df_trips.loc[df_trips["destination_purpose"] == 10, "destination_purpose"] = "other"
    df_trips["purpose"] = df_trips["destination_purpose"].astype("category")




    df_trips.loc[df_trips["mode"] == 1, "mode"] = "walk"
    df_trips.loc[df_trips["mode"] == 2, "mode"] = "walk" #mb chnaged this to walk
    df_trips.loc[df_trips["mode"] == 3, "mode"] = "pt"
    df_trips.loc[df_trips["mode"] == 4, "mode"] = "pt"
    df_trips.loc[df_trips["mode"] == 5, "mode"] = "pt"
    df_trips.loc[df_trips["mode"] == 6, "mode"] = "pt"
    df_trips.loc[df_trips["mode"] == 7, "mode"] = "mc"
    df_trips.loc[df_trips["mode"] == 8, "mode"] = "car"
    df_trips.loc[df_trips["mode"] == 9, "mode"] = "car"
    df_trips.loc[df_trips["mode"] == 10, "mode"] = "mc"
    df_trips.loc[df_trips["mode"] == 11, "mode"] = "car"
    df_trips.loc[df_trips["mode"] == 12, "mode"] = "mc"
    df_trips.loc[df_trips["mode"] == 13, "mode"] = "car"

    df_trips["mode"] = df_trips["mode"].astype("category")

    

    ### delete person that are not start at home

    g = df_trips.groupby('person_id')
    df = g.head(1)
    df1 = df[df.destination_purpose == 'home'] 
    df2 = g.tail(1)
    df2 = df2[df2.destination_purpose != 'home'] 
    df3 = pd.concat([df1, df2]).sort_values(by = "person_id")[["person_id"]].drop_duplicates()

    df_trips['exist1'] = df_trips['person_id'].isin(df3['person_id']) 
    df_trips = df_trips[df_trips['exist1']==False]

    #print(df_trips.count)
    #exit()

    #df_trips["departure_time"] = df_trips["departure_h"] * 3600.0 + df_trips["departure_m"] * 60.0
    #df_trips["arrival_time"] = df_trips["arrival_h"] * 3600.0 + df_trips["arrival_m"] * 60.0

    # Crowfly distance
    df_trips["crowfly_distance"] = np.sqrt(
        (df_trips["origin_coord_x2"] - df_trips["destination_coord_x2"])**2 + (df_trips["origin_coord_y2"] - df_trips["destination_coord_y2"])**2
    )

    # Adjust trip id
    df_trips = df_trips.sort_values(by = ["person_id", "trip_id"])
    #trips_per_person = df_trips.groupby("person_id").size().reset_index(name = "count")["count"].values
    #df_trips["new_trip_id"] = np.hstack([np.arange(n) for n in trips_per_person])

    

    # Impute activity duration
    #df_duration = pd.DataFrame(df_trips[[
    #    "person_id", "trip_id", "arrival_time"
    #]], copy = True)

    #df_following = pd.DataFrame(df_trips[[
    #    "person_id", "trip_id", "departure_time"
    #]], copy = True)
    #df_following.columns = ["person_id", "trip_id", "following_trip_departure_time"]
    #df_following["trip_id"] = df_following["trip_id"] - 1



    df_trips['following_trip_departure_time'] = (
    df_trips.groupby('person_id')['departure_time'].transform(lambda s: s[::-1]))


    #print(df_trips.columns)
    #exit()


    #df_duration = pd.merge(df_duration, df_following, on = ["person_id", "trip_id"])

    #print(df_duration.count)
    #exit()
    

    
    df_trips["activity_duration"] = df_trips["following_trip_departure_time"] - df_trips["arrival_time"]
    df_trips.loc[df_trips["activity_duration"] < 0.0, "activity_duration"] += 24.0 * 3600.0

    #df_duration = df_duration[["person_id", "trip_id", "activity_duration"]]
    #df_trips = pd.merge(df_trips, df_duration, how = "left", on = ["person_id", "trip_id"])

    #print(df_trips.count)
    #exit()


    # Clean up
    df_trips = df_trips[[
        "household_id", "person_id", "trip_id", "origin_coord_x2", "origin_coord_y2",
        "destination_coord_x2", "destination_coord_y2", "purpose",
      "departure_time", "arrival_time", "mode", "trip_network_distance", "weekday","crowfly_distance", "activity_duration"
    ]]

    
    df_persons['exist1'] = df_persons['person_id'].isin(df3['person_id']) 
    df_persons = df_persons[df_persons['exist1']==False]

    #print(df_persons.count)
    #exit()


    # Find everything that is consistent
    existing_ids = set(np.unique(df_persons["person_id"])) & set(np.unique(df_trips["person_id"]))
    df_persons = df_persons[df_persons["person_id"].isin(existing_ids)]
    df_trips = df_trips[df_trips["person_id"].isin(existing_ids)]

    #### From here everything as Paris

    # Contains car
    df_cars = df_trips[df_trips["mode"] == "car"][["person_id"]].drop_duplicates()
    df_cars["has_car_trip"] = True
    df_persons = pd.merge(df_persons, df_cars, how = "left")
    df_persons["has_car_trip"] = df_persons["has_car_trip"].fillna(False)

    # Primary activity information
    df_education = df_trips[df_trips["purpose"] == "education"][["person_id"]].drop_duplicates()
    df_education["has_education_trip"] = True
    df_persons = pd.merge(df_persons, df_education, how = "left")
    df_persons["has_education_trip"] = df_persons["has_education_trip"].fillna(False)

    df_work = df_trips[df_trips["purpose"] == "work"][["person_id"]].drop_duplicates()
    df_work["has_work_trip"] = True
    df_persons = pd.merge(df_persons, df_work, how = "left")
    df_persons["has_work_trip"] = df_persons["has_work_trip"].fillna(False)

    # Find commute information
    df_commute = df_trips[df_trips["purpose"].isin(["work", "education"])]
    df_commute = df_commute.sort_values(by = ["person_id", "crowfly_distance"])
    df_commute = df_commute.drop_duplicates("person_id", keep = "last")

    df_commute = df_commute[["person_id", "crowfly_distance", "mode"]]
    df_commute.columns = ["person_id", "commute_distance", "commute_mode"]

    df_persons = pd.merge(df_persons, df_commute, on = "person_id", how = "left")

    assert(not df_persons[df_persons["has_work_trip"]]["commute_distance"].isna().any())
    assert(not df_persons[df_persons["has_education_trip"]]["commute_distance"].isna().any())

    # Passengers

    #df_passenger = pd.DataFrame(df_trips[["person_id", "mode"]], copy = True)
    #df_passenger = df_passenger[df_passenger["mode"] == "car_passenger"][["person_id"]]
    #df_passenger = df_passenger.drop_duplicates()
    #df_passenger["is_passenger"] = True

    #df_persons = pd.merge(df_persons, df_passenger, on = "person_id", how = "left")
    #df_persons["is_passenger"] = df_persons["is_passenger"].fillna(False)
    #df_persons["is_passenger"] = df_persons["is_passenger"].astype(np.bool)

    #print(df_trips.count)
    #exit()


    return df_persons, df_trips
