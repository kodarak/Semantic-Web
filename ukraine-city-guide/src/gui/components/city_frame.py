import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import logging

from src.data.database import Database

logger = logging.getLogger(__name__)

class CityFrame(ctk.CTkFrame):
    def __init__(self, master, main_window):
        super().__init__(master)
        self.db = Database()
        self.main_window = main_window

        # Створюємо текстове поле для інформації
        self.info_text = ctk.CTkTextbox(
            self,
            wrap="word",
            font=("Arial", 12)
        )
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Створюємо фрейм для кнопок
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        # Кнопка для відкриття Wikipedia
        self.wiki_button = ctk.CTkButton(
            button_frame,
            text="Відкрити у Wikipedia",
            command=self.open_wiki
        )
        self.wiki_button.pack(side="left", padx=5)

        # Кнопка для збереження
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Зберегти",
            command=self.save_city
        )
        self.save_button.pack(side="left", padx=5)

    def update_info(self, city_info: dict):
        text = "Інформація про місто відсутня"

        if city_info:
            population = city_info.get('population')
            if population:
                population = f"{population:,}".replace(",", " ")
            else:
                population = "Невідомо"

            text = f"""
    Місто: {city_info.get('name', 'Невідомо')}

    Загальна інформація:
    - Населення: {population} осіб

    Розташування:
    - Широта: {city_info.get('latitude', 'Невідомо')}
    - Довгота: {city_info.get('longitude', 'Невідомо')}

    Опис:
    {city_info.get('description', 'Опис відсутній')}
            """

        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", text)

    def open_wiki(self):
        if self.main_window.get_current_city():
            city_name = self.main_window.get_current_city()['name']
            if city_name:
                url = f"https://uk.wikipedia.org/wiki/{city_name}"
                webbrowser.open(url)

    def save_city(self):
        if self.main_window.get_current_city():
            try:
                success = self.db.add_city(self.main_window.get_current_city())
                if success:
                    messagebox.showinfo(
                        "Успіх",
                        f"Місто {self.main_window.get_current_city()['name']} успішно збережено"
                    )
                else:
                    messagebox.showerror(
                        "Помилка",
                        "Не вдалося зберегти місто"
                    )
            except Exception as e:
                logger.error(f"Error saving city: {e}")
                messagebox.showerror(
                    "Помилка",
                    f"Помилка при збереженні: {str(e)}"
                )
