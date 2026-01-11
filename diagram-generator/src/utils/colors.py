def get_color(color_name):
    color_map = {
        "primary": "#3498db",  # Blue
        "secondary": "#2ecc71",  # Green
        "background": "#ecf0f1",  # Light Gray
        "text": "#2c3e50",  # Dark Gray
        "highlight": "#e74c3c",  # Red
    }
    return color_map.get(color_name.lower(), "#000000")  # Default to black if not found

def is_valid_color(color_name):
    return color_name.lower() in {
        "primary", "secondary", "background", "text", "highlight"
    }