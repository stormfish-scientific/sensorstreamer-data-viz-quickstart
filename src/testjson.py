import json
import argparse

from pprint import pprint

parser = argparse.ArgumentParser('test json file')

parser.add_argument('json_file')

args = parser.parse_args()

with open(args.json_file, 'r') as jf:
    filedata = jf.read()

data = json.loads(filedata)

pprint(data[0])

print(len(data))


