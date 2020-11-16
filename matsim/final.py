import shutil
import os.path

def configure(context, require):
    require.stage("matsim.run")
    require.config("output_path")
    require.config("output_id")

def execute(context):
    results_path = context.stage("matsim.run")

    output_path = context.config["output_path"]
    output_id = context.config["output_id"]

    if not os.path.isdir(output_path):
        raise RuntimeError("Output path does not exist:", output_path)

    target_path = "%s/%s" % (output_path, output_id)

    if os.path.exists(target_path):
        if os.path.isdir(target_path):
            print("Cleaning target directory:", target_path)
            shutil.rmtree(target_path)
        else:
            raise RuntimeError("Cannot clean target path:", target_path)

    os.mkdir(target_path)

    for file in [
        "jakarta_network.xml.gz",
        "transit_schedule_cleaned.xml.gz",
        "transit_vehicles.xml.gz",
        "facilities.xml.gz",
	"mode-vehicles.xml",
        "jakarta_households.xml.gz",
        "jakarta_population.xml.gz",
        "jakarta_config.xml"
    ]:
        shutil.copyfile("%s/%s" % (results_path, file), "%s/%s" % (target_path, file))

    return {}
