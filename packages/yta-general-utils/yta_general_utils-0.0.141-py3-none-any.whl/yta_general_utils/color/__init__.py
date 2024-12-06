from yta_general_utils.color.utils import is_hexadecimal_color, parse_rgba_color, parse_rgb_color
from yta_general_utils.color.converter import ColorConverter
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.color.enums import ColorString
from typing import Union


class Color:
    """
    Class that represents a color, stored as RGBA, makes
    easy the way we interact with color and provide them as
    parameters and simplify the color conversion. The color
    is stored as a not-normalized color, but values can be
    normalized through the methods that allow it (those 
    including the 'normalized' bool parameter).

    Any attribute has to be initialized with a value between
    0 and 255. Alpha as 255 means full opaque.

    TODO: Please confirm alpha 255 is opaque.
    """
    r: int
    """
    Red color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    g: int
    """
    Green color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    b: int
    """
    Blue color, from 0 to 255, where 0 is no value and 255
    is everything.
    """
    a: int
    """
    Alpha (transparency), from 0 to 255, where 0 is no
    value and 255 is everything.
    """
    def __init__(self, r, g, b, a):
        self.r, self.g, self.b, self.a = r, g, b, a

    def as_rgb(self, normalized: bool = False):
        """
        Return the color as a tuple of the 3 rgb values
        that are, in order: red, green and blue.
        """
        if normalized:
            return self.r / 255.0, self.g / 255.0, self.b / 255.0
        
        return self.r, self.g, self.b
    
    def as_rgba(self, normalized: bool = False):
        """
        Return the color as a tuple of the 4 rgba values
        that are, in order: red, green, blue and alpha.
        """
        if normalized:
            return self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0
        
        return self.r, self.g, self.b, self.a

    def as_rgb_array(self, normalized: bool = False):
        """
        Return the color as an array of the 3 rgb values
        that are, in order: red, green and blue.
        """
        return [*self.as_rgb(normalized)]
    
    def as_rgba_array(self, normalized: bool = False):
        """
        Return the color as an array of the 4 rgba values
        that are, in order: red, green, blue and alpha.
        """
        return [*self.as_rgba(normalized)]
    
    def as_hex(self, do_include_alpha: bool = False):
        """
        Return the color as a string represening it in
        hexadecimal value. The result will be #RRGGBB if
        'do_include_alpha' is False, or #RRGGBBAA if
         True.
        """
        return ColorConverter.rgba_to_hex(self.as_rgba(), do_include_alpha)
    
    def as_hsl(self):
        # TODO: Explain
        return ColorConverter.rgba_to_hsl(self.as_rgba())
    
    def as_cymk(self):
        # TODO: Explain
        return ColorConverter.rgba_to_cymk(self.as_rgba())
    
    # TODO: Use the cv2 library to make other changes
    @staticmethod
    def parse(color: Union[list, tuple, str, 'ColorString', 'Color']):
        """
        Parse the provided 'color' parameter and return the
        color as r,g,b,a values or raises an Exception if it
        is not a valid and parseable color.

        This method accepts string colors (if names are
        registered in our system), hexadecimal colors (than
        can also include alpha value), RGB array or tuples
        (that can be normalized, with float values between
        0.0 and 1.0, or not normalized, with int values
        between 0 and 255), or RGBA array or tuples, similar
        to RGB but including a 4h alpha value.
        """
        if PythonValidator.is_instance(color, Color):
            return color

        string_color = None
        try:
            string_color = ColorString.to_enum(color)
        except:
            pass

        color_array = None
        if string_color is not None:
            color_array = ColorConverter.hex_to_rgba(string_color.value)
        elif PythonValidator.is_string(color) and is_hexadecimal_color(color):
            color_array = ColorConverter.hex_to_rgba(color)
        else:
            try:
                color_array = parse_rgba_color(color)
            except:
                pass

            try:
                color_array = *parse_rgb_color(color), 0
            except:
                pass

            if color_array is None:
                raise Exception(f'The provided "color" parameter is not parseable.')
        
        return Color(*color_array)
