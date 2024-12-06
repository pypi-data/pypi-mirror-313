from yta_general_utils.color.utils import is_hexadecimal_color, parse_rgb_color, parse_rgba_color
from typing import Union


class ColorConverter:
    """
    Class to simplify and encapsulate the functionality related
    to color conversion.
    """
    @staticmethod
    def rgb_to_hex(red, green, blue):
        """
        Returns the provided RGB color as a hex color. The 'red', 'green' and
        'blue' parameters must be between 0 and 255.
        """
        return '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    
    @staticmethod
    def hex_to_rgb(color: str):
        """
        Parse the provided hexadecimal 'color' parameter and
        turn it into an RGB color (returned as r,g,b) or
        raises an Exception if not.
        """
        r, g, b, _ = ColorConverter.hex_to_rgba(color)

        return r, g, b

    @staticmethod
    def hex_to_rgba(color: str):
        if not is_hexadecimal_color(color):
            raise Exception(f'The provided "color" parameter "{str(color)}" is not an hexadecimal color.')
        
        # Hex can start with '0x', '0X' or '#'
        hex = color.lstrip('#').lstrip('0x').lstrip('0X')
        if len(hex) == 8:
            # hex with alpha
            r, g, b, a = (int(hex[i:i+2], 16) for i in (0, 2, 4, 6))
        elif len(hex) == 6:
            # hex without alpha
            r, g, b, a = *(int(hex[i:i+2], 16) for i in (0, 2, 4)), 0
        
        return r, g, b, a

    def rgb_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
        """
        Parse the provided RGB 'color' parameter and turn it to
        a hexadecimal color if valid or raises an Exception if
        not. The result will be #RRGGBB if 'do_include_alpha' is
        False, or #RRGGBBAA if 'do_include_alpha' is True.
        """
        r, g, b = parse_rgb_color(color)

        hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
        if do_include_alpha:
            hex = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, 0)

        return hex
        
    def rgba_to_hex(color: Union[tuple, list], do_include_alpha: bool = False):
        """
        Parse the provided RGBA 'color' parameter and turn it to
        a hexadecimal color if valid or raises an Exception if
        not. The result will be #RRGGBB if 'do_include_alpha' is
        False, or #RRGGBBAA if 'do_include_alpha' is True.
        """
        r, g, b, a = parse_rgba_color(color)

        hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
        if do_include_alpha:
            hex = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

        return hex

    def rgba_to_hsl(color: Union[tuple, list]):
        # TODO: Explain
        _, _, _, a = parse_rgba_color(color)
        
        return *ColorConverter.rgb_to_hsl(color), a

    def rgb_to_hsl(color: Union[tuple, list]):
        # TODO: Explain
        r, g, b = parse_rgb_color(color)
        # Normalizamos los valores de r, g, b de 0-255 a 0-1
        r /= 255.0
        g /= 255.0
        b /= 255.0
        
        # Encuentra los valores máximos y mínimos de los componentes RGB
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        # Calcular el tono (H)
        if delta == 0:
            h = 0  # Si no hay diferencia, el tono es indefinido (gris)
        elif cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        else:  # cmax == b
            h = (60 * ((r - g) / delta) + 240) % 360
        
        # Calcular la luminosidad (L)
        l = (cmax + cmin) / 2
        
        # Calcular la saturación (S)
        if delta == 0:
            s = 0  # Si no hay diferencia, la saturación es 0 (gris)
        else:
            s = delta / (1 - abs(2 * l - 1)) if l != 0 and l != 1 else delta / (2 - (cmax + cmin))

        # TODO: I saw in some online solutions that they offer
        # the results without decimal figures
        return round(h, 2), round(s * 100, 2), round(l * 100, 2)

    def rgba_to_cymk(color: Union[tuple, list]):
        # TODO: Explain
        # TODO: Is there a way to handle alpha transparency
        # with a cymk (?)
        return ColorConverter.rgb_to_cymk(color)

    def rgb_to_cymk(color: Union[tuple, list]):
        # TODO: Explain
        # It looks like you need to know the color profile before
        # any conversion from RGB or RGBA
        # https://www.reddit.com/r/AdobeIllustrator/comments/17vpbod/different_cmyk_values_for_same_hex_code_which/?rdt=55781#:~:text=A%20hex%20code%20is%20an,information%2C%20like%20a%20colour%20profile.
        r, g, b = parse_rgb_color(color)
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        k = 1 - max(r, g, b)

        if k == 1:
            c = m = y = 0
        else:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)

        # TODO: I saw in some online solutions that they offer
        # the results without decimal figures
        return round(c * 100, 2), round(m * 100, 2), round(y * 100, 2), round(k * 100, 2)
    
