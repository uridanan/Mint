import json

def loadjsondata(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data


ENV_FILE = 'src/env.json'
env = loadjsondata(ENV_FILE)

