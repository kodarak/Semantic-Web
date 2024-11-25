import pytest
import os
import tempfile
from src.data.database import Database

@pytest.fixture
def sample_city_data():
    return {
        'name': 'Kyiv',
        'population': 2967360,
        'description': 'Capital of Ukraine',
        'latitude': 50.4501,
        'longitude': 30.5234,
        'region': 'Kyiv Oblast'
    }

@pytest.fixture
def valid_coordinates():
    return (50.4501, 30.5234)

@pytest.fixture(scope="function")
def test_db():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_db_path = tmp.name

    db = Database(temp_db_path)
    yield db

    db.close()
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)
