"""
Service for fetching data from Wikidata
"""
import logging
from typing import List, Optional, Dict
from SPARQLWrapper import SPARQLWrapper, JSON

logger = logging.getLogger(__name__)

class WikidataService:
    def __init__(self):
        self.endpoint = "http://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.endpoint)

    def get_city_info(self, city_name: str) -> Optional[Dict]:
        """
        Отримання інформації про місто з Wikidata
        
        Args:
            city_name: Назва міста
            
        Returns:
            Optional[Dict]: Інформація про місто або None
        """
        try:
            query = """
            SELECT ?city ?cityLabel ?population ?area ?elevation ?coord ?description
            WHERE {
              ?city rdfs:label "%s"@uk;
                    wdt:P31 wd:Q515;  # instance of city
                    wdt:P17 wd:Q212.  # located in Ukraine
              
              OPTIONAL { ?city wdt:P1082 ?population . }
              OPTIONAL { ?city wdt:P2046 ?area . }
              OPTIONAL { ?city wdt:P2044 ?elevation . }
              OPTIONAL { ?city wdt:P625 ?coord . }
              OPTIONAL { 
                ?city schema:description ?description .
                FILTER(LANG(?description) = "uk")
              }
              
              SERVICE wikibase:label { bd:serviceParam wikibase:language "uk". }
            }
            """ % city_name

            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()
            
            if results["results"]["bindings"]:
                result = results["results"]["bindings"][0]
                return {
                    'name': city_name,
                    'population': int(result["population"]["value"]) if "population" in result else None,
                    'area': float(result["area"]["value"]) if "area" in result else None,
                    'elevation': int(result["elevation"]["value"]) if "elevation" in result else None,
                    'description': result["description"]["value"] if "description" in result else None,
                    'coordinates': self._parse_coordinates(result["coord"]["value"]) if "coord" in result else None
                }
            return None
            
        except Exception as e:
            logger.error(f"Error fetching data from Wikidata: {e}")
            return None

    def search_cities(self, query: str) -> List[str]:
        """
        Пошук міст за запитом
        
        Args:
            query (str): Пошуковий запит
            
        Returns:
            List[str]: Список знайдених міст
        """
        try:
            sparql_query = """
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT DISTINCT ?cityLabel
            WHERE {
                ?city wdt:P31 wd:Q515 ;        # instance of city
                      wdt:P17 wd:Q212 ;        # country Ukraine
                      rdfs:label ?cityLabel .
                FILTER(LANG(?cityLabel) = "uk") # Ukrainian labels only
                FILTER(CONTAINS(LCASE(str(?cityLabel)), LCASE("%s")))
            }
            ORDER BY ?cityLabel
            LIMIT 10
            """ % query
            
            self.sparql.setQuery(sparql_query)
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()
            return [result["cityLabel"]["value"] for result in results["results"]["bindings"]]
            
        except Exception as e:
            logger.error(f"Error searching cities in Wikidata: {e}")
            return []
        
    def _parse_coordinates(self, coord_str: str) -> Optional[Dict[str, float]]:
        """Parse coordinates from Wikidata format"""
        try:
            import re
            match = re.search(r'Point\(([-\d.]+) ([-\d.]+)\)', coord_str)
            if match:
                return {
                    'longitude': float(match.group(1)),
                    'latitude': float(match.group(2))
                }
            return None
        except Exception:
            return None
