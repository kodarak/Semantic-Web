"""
Database fixtures for testing
"""
import pytest
from src.data.database import Database

@pytest.fixture
def test_db():
    """Фікстура для тестової бази даних"""
    db = Database("test.db")
    db.init_db()
    yield db
    # Cleanup після тестів

@pytest.fixture
def sample_city_data():
    """Тестові дані міста"""
    return {
        'name': 'Тестове Місто',
        'population': 100000,
        'description': 'Тестовий опис',
        'latitude': 50.0,
        'longitude': 30.0
    }