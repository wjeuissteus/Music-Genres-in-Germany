#! usr/bin/env python

from sys import argv
from os.path import exists
import simplejson as json 
#import json as simplejson
#import simplejson as json to import jsons

script, in_file, out_file = argv

data = json.load(open(in_file))
for key in data:
    print data[key]["coordinates"][1]


geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": data[key]["coordinates"]
            },
        "properties" : key,
     } for key in data]
}


output = open(out_file, 'w')
json.dump(geojson, output)

print geojson