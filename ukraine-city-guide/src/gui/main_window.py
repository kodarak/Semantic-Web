import customtkinter as ctk
from tkinter import messagebox
import logging

import numpy as np
from src.data.database import Database
from src.services.sparql_service import SPARQLService
from src.services.city_service import CityService
from .components.city_frame import CityFrame
from .components.map_frame import MapFrame

import matplotlib
matplotlib.use('Agg')  # Використовуємо backend без GUI
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)
        
class MainWindow:
    def __init__(self, master):
        self.root = master
        self.city_service = CityService()
        self.sparql_service = SPARQLService()
        self.current_city = None
        self.db = Database()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.setup_ui()
        
    def setup_ui(self):
        try:
            self.setup_left_panel()
            self.setup_right_panel()
            self.setup_stats_tab()
        except Exception as e:
            logger.error(f"Error setting up UI: {e}")
            messagebox.showerror("Помилка", "Помилка при створенні інтерфейсу")
        
        # Кнопка видалення бази даних
        delete_db_button = ctk.CTkButton(
            self.left_panel,
            text="Видалити базу даних",
            command=self.delete_database
        )
        delete_db_button.pack(pady=(20, 10))
    

    def delete_database(self):
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете очистити базу даних?"):
            self.db.clear_database()
            self.update_statistics()
    
    def setup_filters(self):
        """Налаштування фільтрів пошуку"""
        filters_frame = ctk.CTkFrame(self.left_panel)
        filters_frame.pack(padx=10, pady=5, fill="x")
        
        # Населення
        population_frame = ctk.CTkFrame(filters_frame)
        population_frame.pack(padx=5, pady=5, fill="x")
        
        ctk.CTkLabel(population_frame, text="Населення").pack()
        
        # Створюємо контейнер для полів вводу
        pop_entries = ctk.CTkFrame(population_frame)
        pop_entries.pack(fill="x", padx=5)
        
        # Поля вводу населення (змінено імена атрибутів)
        self.min_population_entry = ctk.CTkEntry(
            pop_entries,
            placeholder_text="від",
            width=80
        )
        self.min_population_entry.pack(side="left", padx=2)
        
        self.max_population_entry = ctk.CTkEntry(
            pop_entries,
            placeholder_text="до",
            width=80
        )
        self.max_population_entry.pack(side="right", padx=2)
        
        # Кнопка пошуку за населенням
        ctk.CTkButton(
            population_frame,
            text="Пошук за населенням",
            command=self.search_by_population
        ).pack(pady=5)
        
        # Площа
        area_frame = ctk.CTkFrame(filters_frame)
        area_frame.pack(padx=5, pady=5, fill="x")
        
        ctk.CTkLabel(area_frame, text="Площа (км²)").pack()
        
        # Контейнер для полів вводу площі
        area_entries = ctk.CTkFrame(area_frame)
        area_entries.pack(fill="x", padx=5)
        
        # Поля вводу площі (змінено імена атрибутів)
        self.min_area_entry = ctk.CTkEntry(
            area_entries,
            placeholder_text="від",
            width=80
        )
        self.min_area_entry.pack(side="left", padx=2)
        
        self.max_area_entry = ctk.CTkEntry(
            area_entries,
            placeholder_text="до",
            width=80
        )
        self.max_area_entry.pack(side="right", padx=2)
        
        # Кнопка пошуку за площею
        ctk.CTkButton(
            area_frame,
            text="Пошук за площею",
            command=self.search_by_area
        ).pack(pady=5)

    def setup_left_panel(self):
        """Налаштування лівої панелі"""
        self.left_panel = ctk.CTkFrame(self.root)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Заголовок
        title = ctk.CTkLabel(
            self.left_panel,
            text="Гід містами України",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20, padx=10)
        
        # Пошук
        search_frame = ctk.CTkFrame(self.left_panel)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Пошук міста...",
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Пошук",
            command=self.search_city,
            width=60
        )
        self.search_button.pack(side="right")
        
        # Налаштування фільтру за населенням
        self.setup_population_filter()
        
        # Список міст
        cities_label = ctk.CTkLabel(
            self.left_panel,
            text="Популярні міста:",
            font=("Helvetica", 14)
        )
        cities_label.pack(pady=(20, 5))
        
        self.cities_list = ctk.CTkScrollableFrame(self.left_panel)
        self.cities_list.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Оновлення списку міст
        self.update_cities_list()
    
    def setup_right_panel(self):
        self.right_panel = ctk.CTkTabview(self.root)
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Вкладка з інформацією
        self.info_tab = self.right_panel.add("Інформація")
        self.city_frame = CityFrame(self.info_tab, self)
        self.city_frame.pack(fill="both", expand=True)
        
        # Вкладка з картою
        self.map_tab = self.right_panel.add("Карта")
        self.map_frame = MapFrame(self.map_tab)
        self.map_frame.pack(fill="both", expand=True)
        
        # Вкладка зі статистикою
        self.stats_tab = self.right_panel.add("Статистика")
        # TODO: Додати віджети для відображення статистики
    
    def search_city(self):
        """Обробник пошуку міста"""
        query = self.search_entry.get().strip()
        if not query:
            return
            
        try:
            cities = self.city_service.search_cities(query)
            self.update_cities_list(cities)
            
            if not cities:
                messagebox.showinfo(
                    "Пошук",
                    "Міста не знайдені"
                )
                
        except Exception as e:
            logger.error(f"Error searching city: {e}")
            messagebox.showerror(
                "Помилка",
                "Помилка при пошуку міста"
            )
    
    def update_cities_list(self, cities=None):
        """Оновлення списку міст"""
        # Очищення списку
        for widget in self.cities_list.winfo_children():
            widget.destroy()
            
        if cities is None:
            # Завантаження популярних міст
            cities = self.city_service.get_popular_cities()
        
        for city in cities:
            btn = ctk.CTkButton(
                self.cities_list,
                text=city,
                command=lambda c=city: self.show_city_info(c)
            )
            btn.pack(padx=5, pady=2, fill="x")
    
    def show_city_info(self, city_name):
        try:
            city_info = self.city_service.get_city_info(city_name)
            if city_info:
                self.set_current_city(city_info)
                if self.city_frame:
                    self.city_frame.update_info(city_info)
                self.map_frame.update_location(
                    city_info['latitude'],
                    city_info['longitude'],
                    city_name
                )
                self.update_statistics()
            else:
                messagebox.showwarning(
                    "Інформація відсутня",
                    f"Не вдалося знайти інформацію про місто {city_name}"
                )
        except Exception as e:
            logger.error(f"Error showing city info: {e}")
            messagebox.showerror(
                "Помилка",
                f"Помилка при отриманні інформації про місто: {str(e)}"
            )

    def set_current_city(self, city_info):
        self.current_city = city_info
        if self.city_frame:
            self.city_frame.update_info(self.current_city)

    def get_current_city(self):
        return self.current_city
    
    def setup_population_filter(self):
        """Налаштування фільтру за населенням"""
        filter_frame = ctk.CTkFrame(self.left_panel)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Заголовок фільтру
        ctk.CTkLabel(
            filter_frame, 
            text="Фільтр за населенням:",
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        # Поля вводу
        entries_frame = ctk.CTkFrame(filter_frame)
        entries_frame.pack(fill="x", padx=5)
        
        self.min_population_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="від",
            width=80
        )
        self.min_population_entry.pack(side="left", padx=2)
        
        self.max_population_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="до",
            width=80
        )
        self.max_population_entry.pack(side="right", padx=2)
        
        # Кнопка пошуку
        ctk.CTkButton(
            filter_frame,
            text="Фільтрувати",
            command=self.search_by_population
    ).pack(pady=5)

    def search_by_population(self):
        """Пошук міст за населенням"""
        try:
            min_pop = int(self.min_population_entry.get()) if self.min_population_entry.get() else None
            max_pop = int(self.max_population_entry.get()) if self.max_population_entry.get() else None
            
            cities = self.city_service.search_cities_by_population(min_pop, max_pop)
            if cities:
                self.update_cities_list([city['name'] for city in cities])
            else:
                messagebox.showinfo(
                    "Пошук",
                    "Міста не знайдені за вказаними критеріями"
                )
        except ValueError:
            messagebox.showerror(
                "Помилка",
                "Введіть коректні числові значення населення"
            )

    def search_by_area(self):
        """Пошук міст за площею"""
        try:
            min_area = float(self.min_area_entry.get()) if self.min_area_entry.get() else None
            max_area = float(self.max_area_entry.get()) if self.max_area_entry.get() else None
            
            cities = self.city_service.search_cities_by_area(min_area, max_area)
            self.update_cities_list([city['name'] for city in cities])
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числові значення")

    # В MainWindow додаємо метод для налаштування вкладки статистики:

    def setup_stats_tab(self):
        """Налаштування вкладки статистики"""
        self.stats_tab.grid_rowconfigure(0, weight=1)
        self.stats_tab.grid_columnconfigure(0, weight=1)

        self.stats_frame = ctk.CTkFrame(self.stats_tab)
        self.stats_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Загальна статистика
        self.general_stats_frame = ctk.CTkFrame(self.stats_frame)
        self.general_stats_frame.pack(fill="x", padx=10, pady=10)

        self.total_cities_label = ctk.CTkLabel(
            self.general_stats_frame,
            text="Кількість міст у базі: 0",
            font=("Helvetica", 16, "bold")
        )
        self.total_cities_label.pack(pady=5)

        # Графік населення
        self.population_stats_frame = ctk.CTkFrame(self.stats_frame)
        self.population_stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.population_chart_label = ctk.CTkLabel(
            self.population_stats_frame,
            text="Розподіл міст за населенням",
            font=("Helvetica", 16, "bold")
        )
        self.population_chart_label.pack(pady=5)

        self.population_chart = ctk.CTkCanvas(self.population_stats_frame, height=400)
        self.population_chart.pack(fill="both", expand=True, pady=5)

        self.update_stats_button = ctk.CTkButton(
            self.stats_frame,
            text="Оновити статистику",
            command=self.update_statistics
        )
        self.update_stats_button.pack(pady=10)

    def update_statistics(self):
        try:
            stats = self.city_service.get_statistics()

            if stats:
                # Оновлюємо загальну статистику
                self.total_cities_label.configure(
                    text=f"Кількість міст у базі: {stats['total_cities']}"
                )

                # Малюємо графік населення міст
                self.draw_population_chart(stats['cities_data'])
            else:
                messagebox.showinfo(
                    "Статистика відсутня",
                    "Не вдалося отримати статистичні дані."
                )
        except Exception as e:
            logger.error(f"Error updating statistics: {e}")
            messagebox.showerror(
                "Помилка",
                "Помилка при оновленні статистики"
        )

    def draw_population_chart(self, cities_data):
        canvas = self.population_chart
        canvas.delete("all")

        if not cities_data:
            # Якщо дані для графіка відсутні, виводимо повідомлення
            canvas.create_text(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2,
                text="Немає даних для відображення",
                font=("Helvetica", 16)
            )
            return

        # Отримуємо ширину і висоту canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        # Встановлюємо розмір фігури відповідно до розміру canvas
        fig, ax = plt.subplots(figsize=(width/100, height/100))

        # Розділяємо назви міст та значення населення
        cities, populations = zip(*cities_data)
        x = range(len(cities))

        # Визначаємо кольорову гаму
        colors = plt.cm.Blues(np.linspace(0.2, 0.8, len(populations)))

        # Будуємо горизонтальний графік
        ax.barh(x, populations, color=colors)

        # Додаємо підписи осей та назву
        ax.set_yticks(x)
        ax.set_yticklabels(cities)
        ax.set_xlabel('Населення')
        ax.set_title('Населення міст України')

        # Додаємо сітку
        ax.grid(axis='x', color='lightgray', linestyle='-')

        # Конвертуємо графік у TkPhoto об'єкт
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        image = Image.open(buffer)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo
