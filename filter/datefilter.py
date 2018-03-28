from sys import argv
from os.path import exists
from os.path import splitext
import simplejson as json 
#import json as simplejson
#import simplejson as json to import jsons

script, in_file, date_start, date_end = argv

data = json.load(open(in_file))

out_file = splitext(in_file)[0] + '_' + date_start + '_' + date_end + ".json"

data_filtered = {key : value for key,value in data.items() if ("begin" in value and value["begin"].isdigit() and int(date_start) <= int(value["begin"]) <= int(date_end))}
    
output = open(out_file, 'w')
json.dump(data_filtered, output)