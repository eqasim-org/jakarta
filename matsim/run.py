import shutil
import os.path

def configure(context, require):
    require.stage("matsim.population")
    require.stage("matsim.households")
    require.stage("matsim.facilities")
    #require.stage("matsim.network.mapped")
    require.stage("matsim.java.eqasim")
    require.stage("matsim.secondary_locations")
    require.stage("utils.java")

def execute(context):
    # Some files we just copy
    #transit_schedule_path = context.stage("matsim.network.mapped")["schedule"]
    transit_schedule_path = "%s/network/jakarta_transit_schedule.xml.gz" % context.config["raw_data_path"]
    shutil.copyfile(transit_schedule_path, "%s/jakarta_transit_schedule.xml.gz" % context.cache_path)

    #transit_vehicles_path = context.stage("matsim.network.mapped")["vehicles"]
    transit_vehicles_path = "%s/network/jakarta_transit_vehicles.xml.gz" % context.config["raw_data_path"]
    shutil.copyfile(transit_vehicles_path, "%s/jakarta_transit_vehicles.xml.gz" % context.cache_path)


    
    vehicles_vehicles_path = "%s/network/mode-vehicles.xml" % context.config["raw_data_path"]
    shutil.copyfile(vehicles_vehicles_path, "%s/jakarta_mode_vehicles.xml.gz" % context.cache_path)


    
    #households_input_path = context.stage("matsim.households")
    #households_prepared_path = "%s/households.xml.gz" % context.cache_path
    #households_output_path = "%s/jakarta_households.xml.gz" % context.cache_path

    #households_input_path = context.stage("matsim.households")
    #households_output_path = "%s/jakarta_households.xml.gz" % context.cache_path


    households_input_path = "%s/matsim.households_cache/households.xml.gz" % context.config["target_path"]  
    shutil.copyfile(households_input_path, "%s/jakarta_households.xml.gz" % context.cache_path)


    #households_path = context.stage("matsim.households") 
    #shutil.copyfile(households_path, "%s/households.xml.gz" % context.cache_path)

    # Some files we send through the preparation script
    #network_input_path = context.stage("matsim.network.mapped")["network"]
    network_input_path = "%s/network/jakarta_network_3.xml.gz" % context.config["raw_data_path"] #jakarta_network.xml.gz
    network_fixed_path = "%s/jakarta_fixed_network.xml.gz" % context.cache_path
    network_output_path = "%s/jakarta_network.xml.gz" % context.cache_path

    facilities_input_path = context.stage("matsim.facilities")
    facilities_output_path = "%s/jakarta_facilities.xml.gz" % context.cache_path

    population_input_path = context.stage("matsim.secondary_locations")
    population_prepared_path = "%s/jakarta_population.xml.gz" % context.cache_path
    population_output_path = "%s/jakarta_population.xml.gz" % context.cache_path

    config_output_path = "%s/jakarta_config.xml" % context.cache_path

    # Call preparation script
    java = context.stage("utils.java")

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.jakarta.scenario.RunNetworkFixer", [
        "--input-path", network_input_path,
        "--output-path", network_fixed_path
    ], cwd = context.cache_path)

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.core.scenario.preparation.RunPreparation", [
        "--input-facilities-path", facilities_input_path,
        "--output-facilities-path", facilities_output_path,
        "--input-population-path", population_input_path,
        "--output-population-path", population_prepared_path,
        "--input-network-path", network_fixed_path,
        "--output-network-path", network_output_path,
        "--threads", str(context.config["threads"])
    ], cwd = context.cache_path)

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.core.scenario.config.RunGenerateConfig", [
        "--output-path", config_output_path,
        "--prefix", "jakarta_",
        "--sample-size", str(context.config["input_downsampling"]),
        "--random-seed", str(0),
        "--threads", str(context.config["threads"])
    ], cwd = context.cache_path)

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.jakarta.scenario.RunAdaptConfig", [
        "--input-path", config_output_path,
        "--output-path", config_output_path
    ], cwd = context.cache_path)

    #java(
    #    context.stage("matsim.java.eqasim"),
    #    "org.eqasim.core.scenario.routing.RunPopulationRouting", [
    #    "--config-path", config_output_path,
    #    "--output-path", population_output_path,
    #    "--threads", str(context.config["threads"]),
    #    "--config:plans.inputPlansFile", population_prepared_path
    #], cwd = context.cache_path)

    #java(
    #    context.stage("matsim.java.eqasim"),
    #    "org.eqasim.core.scenario.validation.RunScenarioValidator", [
    #    "--config-path", config_output_path
    #], cwd = context.cache_path)

    java(
        context.stage("matsim.java.eqasim"),
        "org.eqasim.jakarta.RunSimulation", [
        "--config-path", config_output_path,
        "--config:controler.lastIteration", str(40),
        "--config:controler.writeEventsInterval", str(1),
        "--config:controler.writePlansInterval", str(10),
    ], cwd = context.cache_path)

    return context.cache_path
