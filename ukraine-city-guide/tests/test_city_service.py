"""
Tests for City Service
"""

import pytest
from src.services.city_service import CityService

@pytest.fixture
def city_service():
    """Fixture for CityService"""
    return CityService()

def test_get_popular_cities(city_service):
    """Test getting list of popular cities"""
    cities = city_service.get_popular_cities()
    assert isinstance(cities, list)
    assert len(cities) > 0
    assert "Київ" in cities

def test_get_city_info(city_service):
    """Test getting city information"""
    info = city_service.get_city_info("Київ")
    assert info is not None
    assert isinstance(info, dict)
    assert info['name'] == "Київ"
    assert 'population' in info
    assert 'description' in info

def test_save_city(city_service):
    """Test saving city information"""
    city_data = {
        'name': 'TestCity',
        'population': 1000000,
        'description': 'Test description',
        'latitude': 50.0,
        'longitude': 30.0
    }
    result = city_service.save_city(city_data)
    assert result is True

def test_search_cities(city_service):
    """Test searching cities"""
    # Додаємо тестові дані
    city_service.save_city({
        'name': 'Київ',
        'population': 3000000
    })
    
    results = city_service.search_cities("Ки")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "Київ" in results

def test_search_by_population(city_service):
    """Test searching cities by population"""
    cities = city_service.search_cities_by_population(min_population=1000000)
    assert isinstance(cities, list)
    for city in cities:
        assert city['population'] >= 1000000

def test_get_nearest_cities(city_service):
    """Test finding nearest cities"""
    cities = city_service.get_nearest_cities(50.4501, 30.5234)  # Координати Києва
    assert isinstance(cities, list)
    assert len(cities) <= 5  # Перевіряємо ліміт
    assert all('distance' in city for city in cities)