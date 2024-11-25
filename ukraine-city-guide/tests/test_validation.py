import pytest
from src.services.city_service import CityService

def test_city_data_validation():
    """Test city data validation"""
    service = CityService()
    
    # Valid data
    valid_data = {
        'name': 'Тест',
        'population': 1000,
        'latitude': 50.0,
        'longitude': 30.0
    }
    assert service.save_city(valid_data)
    
    # Invalid population
    invalid_population = {
        'name': 'Тест',
        'population': 'not a number',
        'latitude': 50.0,
        'longitude': 30.0
    }
    assert not service.save_city(invalid_population)
    
    # Invalid coordinates
    invalid_coordinates = {
        'name': 'Тест',
        'population': 1000,
        'latitude': 'invalid',
        'longitude': 'invalid'
    }
    assert not service.save_city(invalid_coordinates)