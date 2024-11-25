from rdflib import logger
import requests
import json

class OpenDataService:
    """Сервіс для роботи з порталом відкритих даних data.gov.ua"""
    
    def __init__(self):
        self.api_url = "https://data.gov.ua/api/3/action/"
    
    def get_city_data(self, city_name):
        """Отримання даних про місто з порталу відкритих даних"""
        try:
            # API-запит до порталу
            response = requests.get(
                f"{self.api_url}package_search",
                params={"q": city_name}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching data from data.gov.ua: {e}")
            return None
