import requests
from tqdm import tqdm
import subprocess as sp
import os.path

def configure(context, require):
    require.stage("utils.java")

def execute(context):
    java = context.stage("utils.java")

    sp.check_call([
        "git", "clone", "https://github.com/eqasim-org/eqasim-java.git"
    ], cwd = context.cache_path)

    sp.check_call([
        "git", "checkout", "v1.0.1"
    ], cwd = "%s/eqasim-java" % context.cache_path)

    sp.check_call([
        "mvn", "-Pstandalone", "package"
    ], cwd = "%s/eqasim-java" % context.cache_path)

    jar = "%s/eqasim-java/grater_jakarta/target/greater_jakarta-1.0.1.jar" % context.cache_path
    return jar
