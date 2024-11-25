"""
Database tests
"""
def test_add_city(test_db, sample_city_data):
    """Тест додавання міста"""
    assert test_db.add_city(sample_city_data)
    city = test_db.get_city(sample_city_data['name'])
    assert city is not None
    assert city['name'] == sample_city_data['name']