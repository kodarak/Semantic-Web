"""
SPARQL service for fetching data from DBpedia
"""

from rdflib import Graph
from rdflib.plugins.stores import sparqlstore
import logging

logger = logging.getLogger(__name__)

class SPARQLService:
    def __init__(self):
        self.endpoint = "http://dbpedia.org/sparql"
        self.store = sparqlstore.SPARQLStore(query_endpoint=self.endpoint)
        self.graph = Graph(store=self.store)
    
    def get_city_info(self, city_name: str) -> dict:
        try:
            query = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            
            SELECT ?population ?abstract ?lat ?long
            WHERE {
                ?city rdfs:label ?name ;
                    a dbo:City ;
                    dbo:country dbr:Ukraine .
                FILTER(?name = "%s"@uk)
                OPTIONAL { ?city dbo:populationTotal ?population }
                OPTIONAL { ?city dbo:abstract ?abstract . 
                        FILTER(LANG(?abstract) = "uk") }
                OPTIONAL { ?city geo:lat ?lat }
                OPTIONAL { ?city geo:long ?long }
            }
            LIMIT 1
            """ % city_name
            
            results = list(self.graph.query(query))
            if not results:
                return None
                
            result = results[0]
            city_info = {'name': city_name}
            
            # Безпечне отримання значень
            def safe_get(value, convert_func=None):
                try:
                    if hasattr(result, value):
                        val = getattr(result, value)
                        if val is None:
                            return None
                        if convert_func:
                            return convert_func(val.value)
                        return val.value
                    return None
                except Exception as e:
                    logger.error(f"Error converting {value}: {e}")
                    return None
            
            city_info.update({
                'population': safe_get('population', int),
                'description': safe_get('abstract', str),
                'latitude': safe_get('lat', float),
                'longitude': safe_get('long', float)
            })
            
            return city_info
                
        except Exception as e:
            logger.error(f"Error fetching city info: {e}")
            return None

    def search_cities(self, query: str) -> list:
        try:
            sparql_query = """
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?name
            WHERE {{
                ?city a dbo:City ;
                    dbo:country dbr:Ukraine ;
                    rdfs:label ?name .
                FILTER(LANG(?name) = "uk")
                FILTER(CONTAINS(LCASE(str(?name)), LCASE("{}")))
            }}
            ORDER BY ?name
            LIMIT 10
            """.format(query)
            
            results = self.graph.query(sparql_query)
            return [str(result.name) for result in results if result.name]
            
        except Exception as e:
            logger.error(f"Error searching cities: {e}")
            return []
