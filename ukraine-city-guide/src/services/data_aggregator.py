from src.data.database import Database
from src.services.open_data_service import OpenDataService
from src.services.sparql_service import SPARQLService
from src.services.wikidata_service import WikidataService

class DataAggregator:
    """Агрегатор даних з різних джерел"""
    
    def __init__(self):
        self.sparql_service = SPARQLService()
        self.wikidata_service = WikidataService()
        self.open_data_service = OpenDataService()
        self.db = Database()
    
    def merge_data(self, wikidata: dict, gov_data: dict) -> dict:
        """Об'єднання даних з різних джерел"""
        result = wikidata.copy()
        result.update(gov_data)
        return result
    
    def get_city_info(self, city_name):
        """Отримання інформації про місто з усіх доступних джерел"""
        # Спочатку перевіряємо локальну базу
        local_data = self.db.get_city(city_name)
        if local_data:
            return local_data
            
        # Отримуємо дані з Wikidata
        wiki_data = self.wikidata_service.get_city_info(city_name)
        
        # Отримуємо дані з data.gov.ua
        gov_data = self.open_data_service.get_city_data(city_name)
        
        # Об'єднуємо дані
        combined_data = self.merge_data(wiki_data, gov_data)
        
        # Зберігаємо в базу
        if combined_data:
            self.db.add_city(combined_data)
            
        return combined_data
