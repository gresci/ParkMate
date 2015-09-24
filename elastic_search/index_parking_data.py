from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, os

# connect to the elasticsearch instance
es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")

# create index and mapping
if es.indices.exists('geotest'):
    print("deleting index...")
    res = es.indices.delete(index = 'geotest')

os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/')

bb= """curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/geotest/geotest/_mapping -d '{
    "geotest": {
        "properties": {
            "location": {
                "type": "geo_point",
                "lat_lon": true,
                "geohash": true
            }
        }
    }
}'
"""
os.system(bb)


# bulk index and search

bulk_data1 = []

a = """
{"name" : "Rue de Barfleur - Charlesbourg",
"location": {
  "lon": -71.285605,
  "lat": 46.869125
}
}
"""
aa = """
{"name" : "Rue Racine - La Haute-Saint-Charles",
  "location": {
    "lon": -71.356247,
    "lat": 46.855498
  }
  }
"""
b = json.loads(a)
bb = json.loads(aa)

bulk_data1.append(b)
bulk_data1.append(bb)

q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
results = helpers.bulk(es, bulk_data1, index='geotest', doc_type='geotest', refresh=True)

res = es.search(index = 'geotest', size=5, body=q)
print res
