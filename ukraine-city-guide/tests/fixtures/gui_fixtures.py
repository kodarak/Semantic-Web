"""
GUI fixtures for testing
"""
import pytest
import tkinter as tk

@pytest.fixture
def gui_root():
    """Фікстура для тестування GUI"""
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def valid_coordinates():
    """Координати міст для тестів"""
    return {
        'kyiv': (50.4501, 30.5234),
        'lviv': (49.8397, 24.0297)
    }