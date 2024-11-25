"""
Database configuration and operations module
"""

import sqlite3
import logging
import os
from tkinter import messagebox

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name="cities.db"):
        """
        Initialize the database
        
        Args:
            db_name (str): Name of the database file
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_db()

    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.debug("Successfully connected to database")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def init_db(self):
        """Initialize database"""
        try:
            self.connect()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    population INTEGER,
                    description TEXT,
                    latitude REAL,
                    longitude REAL
                )
            ''')
            self.conn.commit()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def search_cities(self, query: str) -> list:
        """
        Search for cities by name
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of found cities
        """
        try:
            self.connect()
            self.cursor.execute('''
                SELECT name FROM cities 
                WHERE name LIKE ? 
            ''', (f'%{query}%',))
            
            results = self.cursor.fetchall()
            return [row[0] for row in results] if results else []
        except Exception as e:
            logger.error(f"Error searching cities: {e}")
            return []
        finally:
            self.close()

    def add_city(self, city_data: dict) -> bool:
        """Add or update city data"""
        try:
            self.connect()
            self.cursor.execute('''
                INSERT OR REPLACE INTO cities 
                (name, population, description, latitude, longitude)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                city_data['name'],
                city_data.get('population'),
                city_data.get('description'),
                city_data.get('latitude'),
                city_data.get('longitude')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding city: {e}")
            return False
        finally:
            self.close()

    def get_city(self, name):
        """Get city information"""
        try:
            self.connect()
            self.cursor.execute('''
                SELECT name, population, description, latitude, longitude 
                FROM cities WHERE name = ?
            ''', (name,))
            result = self.cursor.fetchone()
            if result:
                return {
                    'name': result[0],
                    'population': result[1],
                    'description': result[2],
                    'latitude': result[3],
                    'longitude': result[4]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting city: {e}")
            return None
        finally:
            self.close()

    def clear_database(self):
        try:
            self.connect()
            self.cursor.execute("DELETE FROM cities")
            self.conn.commit()
            logger.info("Database cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
            messagebox.showerror("Помилка", "Не вдалося очистити базу даних")
        finally:
            self.close()
            
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
