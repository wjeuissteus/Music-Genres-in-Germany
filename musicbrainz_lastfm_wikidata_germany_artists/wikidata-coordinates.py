import io
import json
from wikidata_functions import get_coordinates

area_refs = {}  
url_data = {}  
area_url_links = {}
area_coordinates = {}

output_data = {}

# Get the output file of musicbrainz_lastfm_germany_artists.py Script:

with io.open("artists_germany_lastfm.txt", "r") as readfile:
    data = json.load(readfile)

# From MusicBrainz-DUMP: Get "area"-list, "url"-list and list of links between areas and urls

with io.open("area", "r") as file:
    readfile = file.readlines()
    for line in readfile:
        line = line.split("\t")
        if line[3] != 1:
            area_refs[line[1]] = line[0]
        
with io.open("l_area_url", "r") as file:
    readfile = file.readlines()
    for line in readfile:
        line = line.split("\t")
        if line[1] == "118733":
            area_url_links[line[2]] = line[3]
            
with io.open("url", "r") as file:
    readfile = file.readlines()
    for line in readfile:
        line = line.split("\t")
        url_data[line[0]] = line[2].rsplit('/', 1)[-1]           
        
        
# Refine: Save only relevant artist information         
        
for area,artists in data.items():
    print len(artists)
    for artist in artists:
            output_data[artist["id"]] = {}
            if "life-span" in artist:
                if "begin" in artist["life-span"]:
                    output_data[artist["id"]]["begin"] = artist["life-span"]["begin"].rsplit('-')[0]
                if "end" in artist["life-span"]:
                    output_data[artist["id"]]["end"] = artist["life-span"]["end"].rsplit('-')[0]
            output_data[artist["id"]]["area"] = []
            if "area" in artist and artist["area"]["name"] != "Germany":
            	if artist["area"]["id"] not in output_data[artist["id"]]["area"]:
                	output_data[artist["id"]]["area"].append(artist["area"]["id"])
            if "begin-area" in artist and artist["begin-area"]["name"] != "Germany":
            	if artist["begin-area"]["id"] not in output_data[artist["id"]]["area"]:
                	output_data[artist["id"]]["area"].append(artist["begin-area"]["id"])
            if "end-area" in artist and artist["end-area"]["name"] != "Germany":
            	if artist["end-area"]["id"] not in output_data[artist["id"]]["area"]:
                	output_data[artist["id"]]["area"].append(artist["end-area"]["id"])
            output_data[artist["id"]]["tags"] = artist["tags"]
            output_data[artist["id"]]["name"] = artist["name"]
            if "type" in artist:
                output_data[artist["id"]]["type"] = artist["type"]
            if "gender" in artist:
                output_data[artist["id"]]["gender"] = artist["gender"] 
                
            if len(output_data[artist["id"]]["area"]) == 1:  
                output_data[artist["id"]]["area"] = output_data[artist["id"]]["area"][0]
                try:
                    output_data[artist["id"]]["area_wikidata"] = url_data[area_url_links[area_refs[output_data[artist["id"]]["area"]]]]
                except:
                    print area_refs[output_data[artist["id"]]["area"]],
                    
            # If there is more than one area for an artist, create duplicate artist for each area        
                    
            elif len(output_data[artist["id"]]["area"]) > 1:
                for area in output_data[artist["id"]]["area"]:
                    output_data[artist["id"]+"_"+area] = {}
                    for key,value in output_data[artist["id"]].items():
                        if key != "area":
                            output_data[artist["id"]+"_"+area][key] = value
                    output_data[artist["id"]+"_"+area]["area"] = area
                    try:
                        output_data[artist["id"]+"_"+area]["area_wikidata"] = url_data[area_url_links[area_refs[area]]]
                    except:
                        print area_refs[area],
                del output_data[artist["id"]]    
                
print len(output_data.keys())
                
for artist,artist_data in output_data.items():

    # If artist has no area information, delete artist

    if "area_wikidata" not in artist_data:
        del output_data[artist]
        
    # Get area coordinates from Wikidata    
        
    else:
        try:
            if artist_data["area_wikidata"] in area_coordinates:
                artist_data["coordinates"] = area_coordinates[artist_data["area_wikidata"]]
                print ".",
            else:
                artist_data["coordinates"] = get_coordinates(artist_data["area_wikidata"])
                area_coordinates[artist_data["area_wikidata"]] = artist_data["coordinates"]
                print ".",
        except:
            print artist_data["area_wikidata"],                                                              
            print artist_data["name"],
            del output_data[artist]

print len(output_data.keys())            
            
with io.open('artists_germany_lastfm_refined.txt', 'w', encoding='utf8') as writefile:
    writefile.write(unicode(json.dumps(output_data, ensure_ascii=False)))
