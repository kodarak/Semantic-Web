"""
GUI tests
"""
def test_map_frame(gui_root, valid_coordinates):
    """Тест фрейму карти"""
    from src.gui.components.map_frame import MapFrame
    
    map_frame = MapFrame(gui_root)
    kyiv_coords = valid_coordinates['kyiv']
    map_frame.update_location(kyiv_coords[0], kyiv_coords[1], "Київ")
    
    assert map_frame.city_label.cget("text") == "Місто: Київ"