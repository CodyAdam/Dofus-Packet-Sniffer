import json
import re
from os import listdir
from sys import argv

for file in listdir("input"):
    with open(f'input/{file}', 'r') as file:
        out = {}

        for line in file.readlines():
            rexp = r"(?:\\)(\w*)(?:\.as(?:[a-z]|[A-Z]|[: =])*)(\d*)(?:;)"
            match = re.findall(rexp, line)[0]
            out[match[1]] = match[0]

        with open(f'output/protocolIds.json', 'w') as outfile:
            if "-i" in argv:
                json.dump(out, outfile, indent=2)
            else:
                json.dump(out, outfile)
