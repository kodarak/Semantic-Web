"""
Integration tests
"""

import pytest
from src.services.sparql_service import SPARQLService
from src.services.city_service import CityService
from src.data.database import Database

def test_end_to_end_city_flow():
    """Test complete flow of city information"""
    # Initialize services
    sparql_service = SPARQLService()
    city_service = CityService()
    db = Database()
    
    # Get city info from SPARQL and add mock data
    test_city = {
        'name': 'Тестове Місто',
        'population': 100000,
        'description': 'Тестовий опис',
        'latitude': 50.0,
        'longitude': 30.0
    }
    
    # Save to database
    assert db.add_city(test_city) is True
    
    # Retrieve from database
    stored_info = db.get_city('Тестове Місто')
    assert stored_info is not None
    assert stored_info['name'] == 'Тестове Місто'
    
    # Test search functionality
    db.add_city({'name': 'Київ', 'population': 3000000})
    search_results = db.search_cities("Ки")
    assert "Київ" in search_results

def test_data_consistency():
    """Test data consistency between services"""
    # Використовуємо тестові дані
    test_city = {
        'name': 'Тестове Місто',
        'population': 100000,
        'description': 'Тестовий опис',
        'latitude': 50.0,
        'longitude': 30.0
    }
    
    # Зберігаємо в базу даних
    db = Database()
    db.add_city(test_city)
    
    # Отримуємо дані
    stored_info = db.get_city('Тестове Місто')
    
    # Перевіряємо консистентність
    assert stored_info['name'] == test_city['name']
    assert stored_info['population'] == test_city['population']
    assert stored_info['latitude'] == test_city['latitude']
    assert stored_info['longitude'] == test_city['longitude']