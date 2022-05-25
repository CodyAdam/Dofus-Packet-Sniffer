import json
from os import listdir
from sys import argv

for file in listdir("input"):
    with open(f'input/{file}', 'r') as json_file:
        out = {}
        data = json.load(json_file)
        for obj in data:
            out[obj["id"]] = obj
        with open(f'output/{file}', 'w') as outfile:
            if "-i" in argv:
                json.dump(out, outfile, indent=2)
            else:
                json.dump(out, outfile)
