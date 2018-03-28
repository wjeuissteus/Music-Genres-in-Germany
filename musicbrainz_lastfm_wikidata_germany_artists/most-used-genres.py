import io
import json

with io.open("artists_germany_lastfm_refined.txt", "r") as readfile:
    data = json.load(readfile)
    
tags = {}    
    
for artist,artist_data in data.items():
    for tag in artist_data["tags"]:
        if tag not in tags:
            tags[tag] = 0
        tags[tag] += 1

tags = sorted(((value,key) for (key,value) in tags.items()), reverse=True)

for line in tags:
    with io.open('most_used_genres.csv', 'a', encoding='utf8') as writefile:
        writefile.write(unicode(line[0]))
        for item in line[1:]:
            writefile.write(unicode(',%s' % item))
        writefile.write(unicode('\n'))
    