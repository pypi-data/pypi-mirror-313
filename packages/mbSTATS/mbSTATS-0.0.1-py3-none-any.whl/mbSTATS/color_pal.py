import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def generate_color_palette(n_colors):
    """
    Generate a color palette of length `n_colors` based on a predefined gradient.

    Parameters:
    n_colors (int): The number of colors needed in the palette.

    Returns:
    list: A list of hex color codes.
    """
    # Predefined base colors for the palette (stronger, more visible colors)
    base_colors = ["#E0BBE4", "#D39CD7", "#C57EC3", "#9B59B6", "#8E44AD", "#6C3483", "#4B0082", "#3A0063"]
    # Create a linear color map from the base colors
    cmap = LinearSegmentedColormap.from_list("custom_palette", base_colors, N=256)

    # Generate evenly spaced colors along the colormap
    palette = [cmap(i / (n_colors - 1)) for i in range(n_colors)]

    # Convert RGBA to HEX
    hex_palette = ["#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)) for r, g, b, _ in palette]

    return hex_palette
