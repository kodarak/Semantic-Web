"""
Tests for SPARQL Service
"""

import pytest
from src.services.sparql_service import SPARQLService

@pytest.fixture
def sparql_service():
    """Fixture for SPARQLService"""
    return SPARQLService()

def test_sparql_service_initialization(sparql_service):
    """Test SPARQLService initialization"""
    assert sparql_service.endpoint == "http://dbpedia.org/sparql"
    assert sparql_service.graph is not None

def test_get_city_info(sparql_service):
    """Test getting city information"""
    # Створюємо клас для результату
    class MockResult:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, self.Value(value))

        class Value:
            def __init__(self, value):
                if value is None:
                    self.value = None
                elif isinstance(value, (int, float, str)):
                    self.value = value
                else:
                    self.value = str(value)

    # Мокуємо метод запиту
    def mock_query(query):
        return [MockResult(
            population=2967360,
            abstract='Столиця України',
            lat=50.4501,
            long=30.5234,
            area=605.0,
            foundingDate='988',
            leader='Віталій Кличко',
            website='https://kyivcity.gov.ua',
            elevation=179,
            timezone='Europe/Kiev',
            postalCode='01001',
            areaCode='44',
            populationDensity=3800.0,
            university=['Київський національний університет імені Тараса Шевченка'],
            landmark=['Майдан Незалежності', 'Софіївський собор'],
            industry=['Машинобудування', 'Інформаційні технології']
        )]

    # Зберігаємо оригінальний метод
    original_query = sparql_service.graph.query
    sparql_service.graph.query = mock_query

    try:
        result = sparql_service.get_city_info("Київ")
        assert result is not None
        assert result["population"] == 2967360
        assert result["description"] == 'Столиця України'
        assert result["latitude"] == 50.4501
        assert result["longitude"] == 30.5234
        assert result["area"] == 605.0
        assert result["founded_year"] == '988'
        assert result["mayor"] == 'Віталій Кличко'
        assert result["website"] == 'https://kyivcity.gov.ua'
        assert result["elevation"] == 179
        assert result["timezone"] == 'Europe/Kiev'
        assert result["postal_code"] == '01001'
        assert result["phone_code"] == '44'
        assert result["population_density"] == 3800.0
        assert len(result["universities"]) == 1
        assert len(result["landmarks"]) == 2
        assert len(result["industries"]) == 2
    finally:
        # Відновлюємо оригінальний метод
        sparql_service.graph.query = original_query

def test_get_city_info_invalid_city(sparql_service):
    """Test getting information for non-existent city"""
    result = sparql_service.get_city_info("НенаявнеМісто123")
    assert result is None

def test_search_cities(sparql_service):
    """Test city search functionality"""
    cities = sparql_service.search_cities("Ки")
    assert isinstance(cities, list)
    assert len(cities) > 0
    # Перевіряємо, що є хоча б одне місто, яке містить "Ки"
    assert any("Ки" in city for city in cities)

def test_search_cities_empty_query(sparql_service):
    """Test search with empty query"""
    cities = sparql_service.search_cities("")
    assert isinstance(cities, list)

def test_search_cities_special_chars(sparql_service):
    """Test search with special characters"""
    cities = sparql_service.search_cities("!@#$%")
    assert isinstance(cities, list)
    assert len(cities) == 0