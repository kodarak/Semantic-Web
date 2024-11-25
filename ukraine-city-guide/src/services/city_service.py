"""
Service for managing city data
"""

from typing import List, Dict, Optional
import logging

from numpy import atan2, cos, radians, sin, sqrt
from src.data.database import Database
from src.services.sparql_service import SPARQLService
from src.services.wikidata_service import WikidataService
from src.services.open_data_service import OpenDataService


logger = logging.getLogger(__name__)

class CityService:
    def __init__(self):
        self.db = Database()
        self.sparql_service = SPARQLService()
        self.wikidata_service = WikidataService()
        self.open_data_service = OpenDataService()

    def get_popular_cities(self) -> List[str]:
        """Get list of popular cities"""
        return [
            "Київ", "Львів", "Харків", "Одеса", 
            "Дніпро", "Запоріжжя", "Вінниця", 
            "Полтава", "Черкаси", "Тернопіль"
        ]

    def update_city_data(self, city_name: str) -> bool:
        """
        Оновлення даних про місто з усіх доступних джерел
        
        Args:
            city_name (str): Назва міста
            
        Returns:
            bool: True якщо дані оновлено успішно
        """
        try:
            # Отримуємо дані з усіх джерел
            dbpedia_data = self.sparql_service.get_city_info(city_name)
            wikidata_data = self.wikidata_service.get_city_info(city_name)
            open_data = self.open_data_service.get_city_data(city_name)
            
            # Об'єднуємо дані
            city_data = {
                'name': city_name,
                'source': 'combined'
            }
            
            # Додаємо дані з DBpedia
            if dbpedia_data:
                city_data.update({
                    'population': dbpedia_data.get('population'),
                    'description': dbpedia_data.get('description'),
                    'latitude': dbpedia_data.get('latitude'),
                    'longitude': dbpedia_data.get('longitude'),
                    'area': dbpedia_data.get('area'),
                    'founded_year': dbpedia_data.get('founded_year'),
                    'mayor': dbpedia_data.get('mayor'),
                    'website': dbpedia_data.get('website'),
                    'universities': dbpedia_data.get('universities', []),
                    'landmarks': dbpedia_data.get('landmarks', []),
                    'industries': dbpedia_data.get('industries', [])
                })
            
            # Додаємо дані з Wikidata
            if wikidata_data:
                for key, value in wikidata_data.items():
                    if not city_data.get(key) and value is not None:
                        city_data[key] = value
            
            # Додаємо дані з data.gov.ua
            if open_data and open_data.get('success'):
                city_data['open_data'] = open_data.get('result', {})
            
            # Зберігаємо в базу тільки якщо є хоч якісь дані
            if len(city_data) > 2:  # Більше ніж просто name і source
                return self.db.add_city(city_data)
                
            return False
            
        except Exception as e:
            logger.error(f"Error updating city data: {e}")
            return False
    
    def get_city_info(self, city_name: str) -> Optional[Dict]:
        """Get city information"""
        try:
            # Спочатку перевіряємо в базі даних
            city_info = self.db.get_city(city_name)
            if city_info:
                return city_info

            # Якщо немає в базі, отримуємо з SPARQL
            sparql_info = self.sparql_service.get_city_info(city_name)
            if sparql_info:
                # Зберігаємо в базу
                self.db.add_city(sparql_info)
                return sparql_info
                
            logger.warning(f"No city found with name: {city_name}")
            return None
                
        except Exception as e:
            logger.error(f"Error getting city info: {e}")
            return None
    
    def validate_city_data(self, city_data: dict) -> bool:
        """
        Валідація даних міста
        """
        try:
            if not isinstance(city_data.get('name'), str):
                return False
                
            if city_data.get('population') is not None:
                if not isinstance(city_data['population'], (int, float)):
                    return False
                    
            if city_data.get('latitude') is not None:
                if not isinstance(city_data['latitude'], (int, float)):
                    return False
                    
            if city_data.get('longitude') is not None:
                if not isinstance(city_data['longitude'], (int, float)):
                    return False
                    
            return True
        except Exception:
            return False

    def save_city(self, city_data: dict) -> bool:
        """
        Збереження інформації про місто
        """
        try:
            if not self.validate_city_data(city_data):
                return False
            return self.db.add_city(city_data)
        except Exception as e:
            logger.error(f"Error saving city: {e}")
            return False

    def search_cities(self, query: str) -> List[str]:
        """
        Пошук міст за запитом у всіх доступних джерелах
        
        Args:
            query (str): Пошуковий запит
            
        Returns:
            List[str]: Список знайдених міст
        """
        try:
            all_cities = set()  # Використовуємо set для уникнення дублікатів
            
            # Пошук в локальній базі
            db_results = self.db.search_cities(query)
            all_cities.update(db_results)
            
            # Пошук через DBpedia SPARQL
            sparql_results = self.sparql_service.search_cities(query)
            all_cities.update(sparql_results)
            
            # Пошук через Wikidata
            wikidata_results = self.wikidata_service.search_cities(query)
            all_cities.update(wikidata_results)
            
            # Сортуємо результати
            return sorted(list(all_cities))
            
        except Exception as e:
            logger.error(f"Error searching cities: {e}")
            return []

    def get_popular_cities(self) -> List[str]:
        """
        Отримання списку популярних міст України
        """
        return [
            "Київ",
            "Харків",
            "Одеса",
            "Дніпро",
            "Львів",
            "Запоріжжя",
            "Кривий Ріг",
            "Миколаїв",
            "Вінниця",
            "Полтава"
        ]

    def get_city_statistics(self, city_name: str) -> dict:
        """
        Отримання статистики про місто
        """
        try:
            city_info = self.get_city_info(city_name)
            if not city_info:
                return None
                
            # Розрахунок додаткових статистичних даних
            stats = {
                'population_growth': None,  # Можна додати історичні дані
                'population_percentage': None,  # Відсоток від населення України
                'area_percentage': None,  # Відсоток від площі України
                'universities_count': len(city_info.get('universities', [])),
                'landmarks_count': len(city_info.get('landmarks', [])),
                'industries_count': len(city_info.get('industries', []))
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error getting city statistics: {e}")
            return None
    
    def search_cities_by_population(self, min_population: Optional[int] = None, 
                                  max_population: Optional[int] = None) -> List[dict]:
        """
        Пошук міст за населенням
        
        Args:
            min_population (int, optional): Мінімальне населення
            max_population (int, optional): Максимальне населення
            
        Returns:
            List[dict]: Список міст, що відповідають критеріям
        """
        try:
            self.db.connect()
            query = "SELECT * FROM cities WHERE 1=1"
            params = []
            
            if min_population is not None:
                query += " AND population >= ?"
                params.append(min_population)
                
            if max_population is not None:
                query += " AND population <= ?"
                params.append(max_population)
                
            self.db.cursor.execute(query, params)
            results = self.db.cursor.fetchall()
            
            cities = []
            for row in results:
                cities.append({
                    'name': row[1],
                    'population': row[2],
                    'latitude': row[4],
                    'longitude': row[5]
                })
            
            return cities
            
        except Exception as e:
            logger.error(f"Error searching cities by population: {e}")
            return []
        finally:
            self.db.close()

    def search_cities_by_area(self, min_area: Optional[float] = None, 
                            max_area: Optional[float] = None) -> List[dict]:
        """
        Пошук міст за площею
        
        Args:
            min_area (float, optional): Мінімальна площа
            max_area (float, optional): Максимальна площа
            
        Returns:
            List[dict]: Список міст, що відповідають критеріям
        """
        try:
            self.db.connect()
            query = "SELECT * FROM cities WHERE 1=1"
            params = []
            
            if min_area is not None:
                query += " AND area >= ?"
                params.append(min_area)
                
            if max_area is not None:
                query += " AND area <= ?"
                params.append(max_area)
                
            self.db.cursor.execute(query, params)
            results = self.db.cursor.fetchall()
            
            cities = []
            for row in results:
                cities.append({
                    'name': row[1],
                    'area': row[7],
                    'latitude': row[4],
                    'longitude': row[5]
                })
            
            return cities
            
        except Exception as e:
            logger.error(f"Error searching cities by area: {e}")
            return []
        finally:
            self.db.close()

    def search_cities_by_region(self, region: str) -> List[dict]:
        """
        Пошук міст за регіоном
        
        Args:
            region (str): Назва регіону
            
        Returns:
            List[dict]: Список міст у вказаному регіоні
        """
        try:
            self.db.connect()
            self.db.cursor.execute("""
                SELECT * FROM cities 
                WHERE region LIKE ?
            """, (f"%{region}%",))
            
            results = self.db.cursor.fetchall()
            
            cities = []
            for row in results:
                cities.append({
                    'name': row[1],
                    'region': row[6],
                    'latitude': row[4],
                    'longitude': row[5]
                })
            
            return cities
            
        except Exception as e:
            logger.error(f"Error searching cities by region: {e}")
            return []
        finally:
            self.db.close()

    def get_nearest_cities(self, lat: float, lon: float, limit: int = 5) -> List[dict]:
        """
        Пошук найближчих міст
        
        Args:
            lat (float): Широта точки
            lon (float): Довгота точки
            limit (int): Максимальна кількість міст
            
        Returns:
            List[dict]: Список найближчих міст
        """
        try:
            def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
                """Розрахунок відстані між двома точками за формулою гаверсинусів"""
                R = 6371  # Радіус Землі в км
                
                lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c
                
                return distance
            
            self.db.connect()
            self.db.cursor.execute("SELECT * FROM cities")
            results = self.db.cursor.fetchall()
            
            cities_with_distance = []
            for row in results:
                if row[4] is not None and row[5] is not None:  # latitude and longitude
                    distance = calculate_distance(lat, lon, row[4], row[5])
                    cities_with_distance.append({
                        'name': row[1],
                        'distance': distance,
                        'latitude': row[4],
                        'longitude': row[5]
                    })
            
            # Сортування за відстанню
            cities_with_distance.sort(key=lambda x: x['distance'])
            
            return cities_with_distance[:limit]
            
        except Exception as e:
            logger.error(f"Error finding nearest cities: {e}")
            return []
        finally:
            self.db.close()

    def get_statistics(self) -> dict:
        try:
            self.db.connect()

            # Загальна кількість міст
            self.db.cursor.execute("SELECT COUNT(*) FROM cities")
            total_cities = self.db.cursor.fetchone()[0]

            # Отримуємо дані про міста
            self.db.cursor.execute("""
                SELECT name, population
                FROM cities
                ORDER BY population DESC
            """)

            cities_data = self.db.cursor.fetchall()

            return {
                'total_cities': total_cities,
                'cities_data': cities_data
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'total_cities': 0, 'cities_data': []}
        finally:
            self.db.close()