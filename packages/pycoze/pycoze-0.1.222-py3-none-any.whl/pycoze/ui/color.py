from enum import Enum

class ColorFormat(Enum):
    HEX = "hex"
    RGB = "rgb"
    HSL = "hsl"


def hex_to_rgb(hex_color):
    # Convert HEX to RGB
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsl(rgb):
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    lightness = (max_val + min_val) / 2  # 直接用l容易混淆

    if max_val == min_val:
        h, s = 0, 0
    else:
        d = max_val - min_val
        s = d / (2 - max_val - min_val) if lightness > 0.5 else d / (max_val + min_val)
        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return h, s, lightness
