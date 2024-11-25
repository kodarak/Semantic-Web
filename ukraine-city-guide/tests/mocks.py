"""
Mock classes for testing
"""
from collections import namedtuple

class MockSPARQLResult:
    """Mock для результатів SPARQL запитів"""
    def __init__(self, **kwargs):
        self.Result = namedtuple('Result', kwargs.keys())
        self.result = self.Result(**kwargs)
        
    def __iter__(self):
        yield self.result

class MockDatabase:
    """Mock для бази даних"""
    def __init__(self):
        self.cities = {}
        
    def add_city(self, city_data):
        if 'name' not in city_data:
            return False
        self.cities[city_data['name']] = city_data
        return True
        
    def get_city(self, name):
        return self.cities.get(name)
        
    def search_cities(self, query):
        if not query:
            return []
        return [name for name in self.cities.keys() if query.lower() in name.lower()]

class MockSPARQLService:
    """Mock для SPARQL сервісу"""
    def get_city_info(self, city_name):
        if city_name == "Київ":
            return {
                'name': 'Київ',
                'population': 3000000,
                'latitude': 50.4501,
                'longitude': 30.5234,
                'description': 'Столиця України'
            }
        return None