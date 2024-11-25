import pytest
from src.services.sparql_service import SPARQLService
from src.data.database import Database

def test_sparql_service_error_handling():
    """Test SPARQL service error handling"""
    service = SPARQLService()
    
    # Test with invalid query
    result = service.get_city_info("")
    assert result is None
    
    # Test with special characters
    result = service.get_city_info("!@#$%")
    assert result is None

def test_database_error_handling():
    """Test database error handling"""
    import tempfile
    import os
    
    # Створюємо тимчасовий файл
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_db_path = tmp.name
    
    test_db = Database(temp_db_path)
    
    try:
        # Test adding invalid data
        invalid_city = {'invalid_key': 'value'}
        assert not test_db.add_city(invalid_city)
        
        # Test getting non-existent city
        result = test_db.get_city("NonExistentCity")
        assert result is None
        
        # Test searching with invalid query
        results = test_db.search_cities("")
        assert isinstance(results, list)
        assert len(results) == 0
        
    finally:
        # Закриваємо з'єднання з базою
        test_db.close()
        # Тепер можна безпечно видалити файл
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)