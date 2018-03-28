from sys import argv
from os.path import exists
from os.path import splitext
import simplejson as json 
#import json as simplejson
#import simplejson as json to import jsons

script, in_file = argv[0:2]

tag_list = argv[2:]

data = json.load(open(in_file))

out_file = splitext(in_file)[0] + '_' + '_'.join(tag_list) + ".json"

data_filtered = {}
    
for key,value in data.items():
	tags_data = [tag.lower() for tag in value["tags"]]
	if any(tag in tags_data for tag in tag_list):
		data_filtered[key] = value
    
output = open(out_file, 'w')
json.dump(data_filtered, output)