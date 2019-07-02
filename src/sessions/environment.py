import json
import os

def loadjsondata(filename):
    path = os.getcwd()
    with open(filename) as data_file:
        data = json.load(data_file)
    return data


ENV_FILE = os.getcwd()+'/env.json'
env = loadjsondata(ENV_FILE)

