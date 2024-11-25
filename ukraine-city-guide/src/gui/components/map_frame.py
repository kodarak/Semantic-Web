"""
Frame for displaying map in the application
"""
import customtkinter as ctk
import tkintermapview
import logging
from tkinter import messagebox

logger = logging.getLogger(__name__)

class MapFrame(ctk.CTkFrame):
    """
    Фрейм для відображення карти
    """
    def __init__(self, master):
        super().__init__(master)
        self.current_marker = None
        self.setup_ui()
        
    def setup_ui(self):
        """Налаштування інтерфейсу"""
        # Створюємо контейнер для інформації
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        # Мітка для назви міста
        self.city_label = ctk.CTkLabel(
            self.info_frame,
            text="Оберіть місто зі списку",
            font=("Helvetica", 14)
        )
        self.city_label.pack(pady=5)
        
        # Мітка для координат
        self.coords_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Helvetica", 12)
        )
        self.coords_label.pack(pady=5)

        # Створюємо фрейм для карти
        self.map_frame = ctk.CTkFrame(self)
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Ініціалізуємо віджет карти
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        # Встановлюємо початкові налаштування карти
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}")
        self.map_widget.set_position(48.379433, 31.165581)  # Центр України
        self.map_widget.set_zoom(6)

        # Додаємо кнопку для скидання виду
        self.reset_button = ctk.CTkButton(
            self,
            text="Показати всю Україну",
            command=self.reset_view
        )
        self.reset_button.pack(pady=5)
        
    def update_location(self, lat, lon, city_name):
        """Оновлення локації на карті"""
        try:
            if lat is None or lon is None:
                messagebox.showinfo("Інформація", "Координати міста недоступні")
                self.city_label.configure(text="Оберіть місто зі списку")
                self.coords_label.configure(text="")
                return
                
            self.city_label.configure(text=f"Місто: {city_name}")
            self.coords_label.configure(text=f"Координати: {lat:.4f}, {lon:.4f}")
            
            if self.current_marker:
                self.current_marker.delete()
            
            self.current_marker = self.map_widget.set_marker(
                lat, 
                lon,
                text=city_name
            )
            
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(12)
            
        except Exception as e:
            logger.error(f"Error updating map: {e}")
            messagebox.showerror("Помилка", "Помилка при оновленні карти")
    
    def reset_view(self):
        """Скидання виду карти до всієї України"""
        if self.current_marker:
            self.current_marker.delete()
            self.current_marker = None
            
        self.city_label.configure(text="Оберіть місто зі списку")
        self.coords_label.configure(text="")
        
        self.map_widget.set_position(48.379433, 31.165581)
        self.map_widget.set_zoom(6)
