import colorsys

# Define consistent colors for each state
STATE_COLORS = {
    'S': '#1f77b4',  # Blue (Susceptible)
    'I': '#ff3b3b',  # Red (Infected)
    'R': '#2ca02c',  # Green (Recovered)
}

# Define a default color for unknown states
DEFAULT_COLOR = '#888888'

def get_color_map(states):
    """
    Returns a list of colors corresponding to a list of states.
    """
    return [STATE_COLORS.get(state, DEFAULT_COLOR) for state in states]

def adjust_color_luminance(hex_color, factor):
    """
    Adjusts the brightness of a hex color.
    Used by the Three.js renderer to create depth shading.
    """
    if not hex_color.startswith('#'):
        return hex_color
    
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    # Convert to HSV
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    
    # Adjust Value (Brightness)
    v = max(0.0, min(1.0, v + factor))
    
    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))