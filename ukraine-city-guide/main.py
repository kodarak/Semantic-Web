"""
Ukraine City Guide - Desktop application
Main entry point of the application
"""

import sys
import logging
from pathlib import Path
import customtkinter as ctk
from src.gui.main_window import MainWindow
from src.data.database import Database
from src.utils.logger import setup_logger

# Налаштування логування
setup_logger()
logger = logging.getLogger(__name__)

class App:
    """
    Головний клас додатку, який ініціалізує всі компоненти
    """
    def __init__(self):
        # Налаштування теми
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Ініціалізація бази даних
        self.database = Database()
        self.database.init_db()
        
        # Створення головного вікна
        self.root = ctk.CTk()
        self.root.title("Гід містами України")
        self.root.geometry("1200x800")
        
        # Ініціалізація головного вікна
        self.main_window = MainWindow(self.root)
        
    def run(self):
        """Запуск додатку"""
        try:
            logger.info("Starting the application...")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
            sys.exit(1)

def main():
    """Main function to run the application"""
    try:
        app = App()
        app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()