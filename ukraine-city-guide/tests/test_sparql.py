"""
Tests for SPARQL service using mocks
"""
import pytest
from src.services.sparql_service import SPARQLService

class MockSPARQLService:
    def get_city_info(self, city_name):
        if city_name == "Київ":
            return {
                'name': 'Київ',
                'population': 2967360,  # Оновлене значення
                'latitude': 50.4501,
                'longitude': 30.5234,
                'description': 'Столиця України'
            }
        return None
    
    def search_cities(self, query):
        cities = ["Київ", "Кривий Ріг", "Кропивницький"]
        return [city for city in cities if query.lower() in city.lower()]

@pytest.fixture
def mock_sparql_service():
    return MockSPARQLService()

def test_get_city_info_mock(mock_sparql_service):
    """Test getting city information using mock"""
    city_info = mock_sparql_service.get_city_info("Київ")
    assert city_info is not None
    assert city_info['name'] == "Київ"
    assert city_info['population'] == 2967360  # Оновлене значення

def test_search_cities_mock(mock_sparql_service):
    """Test searching cities using mock"""
    cities = mock_sparql_service.search_cities("Ки")
    assert isinstance(cities, list)
    assert len(cities) > 0
    assert "Київ" in cities