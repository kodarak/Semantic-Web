"""
Service for fetching data from data.gov.ua
"""
import logging
import requests
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class DataGovUaService:
    def __init__(self):
        self.api_base = "https://data.gov.ua/api/3/action/"

    def get_city_info(self, city_name: str) -> Optional[Dict]:
        """
        Отримання інформації про місто з data.gov.ua
        
        Args:
            city_name: Назва міста
            
        Returns:
            Optional[Dict]: Інформація про місто або None
        """
        try:
            # Пошук датасетів про місто
            search_url = f"{self.api_base}package_search"
            params = {
                'q': city_name,
                'fq': 'organization:city-council'
            }
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if data['success'] and data['result']['count'] > 0:
                results = data['result']['results']
                city_data = {
                    'name': city_name,
                    'datasets': [],
                    'organizations': []
                }
                
                for result in results:
                    if city_name.lower() in result['title'].lower():
                        city_data['datasets'].append({
                            'title': result['title'],
                            'url': result['url']
                        })
                        if result['organization']:
                            city_data['organizations'].append(result['organization']['title'])
                
                return city_data
            return None
            
        except Exception as e:
            logger.error(f"Error fetching data from data.gov.ua: {e}")
            return None
