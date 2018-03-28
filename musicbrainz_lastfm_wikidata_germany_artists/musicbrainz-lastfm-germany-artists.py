import musicbrainzngs
import json
import unicodecsv as csv
import io
import pylast

# MusicBrainz authorization:

musicbrainzngs.set_useragent("", "0.1", "")
musicbrainzngs.auth("","")
musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)

# Last.fm authorization:

API_KEY = ""
API_SECRET = ""

username = "putmytrustinyou"
password_hash = pylast.md5("dighum1234!")

lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=, password_hash=)


data = {}

# Area of Germany:

area_id = "85752fda-13c4-31a3-bee5-0e5cb1f51dad"

# Getting all artists within Germany
# each including more specific areas of their activity (cities, regions)

limit = 100
offset = 0
artist_list = []

result = musicbrainzngs.browse_artists(area=area_id, limit=limit)
if "artist-list" in result:
	artist_list_request = result["artist-list"]
	artist_list += artist_list_request
	
while len(artist_list_request) >= limit:
	offset += limit
	result = musicbrainzngs.browse_artists(area=area_id, limit=limit, offset=offset)
	if "artist-list" in result:
		artist_list_request = result["artist-list"]
		artist_list += artist_list_request
	else:
		artist_list_request = None
	print ".",

print len(artist_list)

# Remove artists which have no further information on specific areas:

for artist in artist_list:
	if "begin-area" not in artist:
		try:
			if artist["area"]["id"] == area_id:
				artist_list.remove(artist)
		except:
			print artist
		
print len(artist_list)

data[area_id] = []

# For each artist, get top 10 genre tags from Last.fm:

for artist in artist_list:
		try:
			artist_tags = set()
			artist_lastfm = lastfm.get_artist_by_mbid(artist["id"])
			tags_lastfm = artist_lastfm.get_top_tags(limit=10)
			for tag in tags_lastfm:
				artist_tags.add(unicode(str(tag[0])))
			artist["tags"] = list(artist_tags)
			if len(artist["tags"]) > 0:
				data[area_id].append(artist)
				print ".",
		except:
			print ",",

with io.open('artists_germany_lastfm.txt', 'w', encoding='utf8') as writefile:
    writefile.write(unicode(json.dumps(data, ensure_ascii=False)))