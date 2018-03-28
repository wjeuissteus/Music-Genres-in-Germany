import re

# Init SPARQLWrapper-API for Wikidata

from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Definition of function get_coordinates, used in wikidata_coordinates.py

def get_coordinates(area_id):
	sparql.setQuery("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?coordinates
    WHERE
    {
    wd:%s wdt:P625 ?coordinates
    }""" % area_id)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	longitude = None
	latitude = None
	if len(results["results"]["bindings"]) > 0:
		result = results["results"]["bindings"][0]["coordinates"]["value"]
		longitude = re.findall('([-+]?[\d.]+)', result)[0]
		latitude = re.findall('([-+]?[\d.]+)', result)[1]
	return [float(longitude),float(latitude)]


	





