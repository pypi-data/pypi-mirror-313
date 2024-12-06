from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.color.regex import ColorRegularExpression
from yta_general_utils.color.enums import ColorString


def is_hexadecimal_color(color):
    """
    Check that the 'color' parameter is an hexadecimal
    color.
    """
    return ColorRegularExpression.HEX.parse(color)

def is_string_color(color):
    """
    Check that the 'color' parameter is an string 
    color accepted by our system, whose value is an
    hexadecimal value.
    """
    return ColorString.is_valid(color)

def is_array_or_tuple_without_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are float values between
    0 and 1 (normalized value).
    """
    return is_array_or_tuple_without_alpha and all(PythonValidator.is_instance(c, float) and 0 <= c <= 1 for c in color)

def is_array_or_tuple_with_alpha_normalized(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are float values between
    0 and 1 (normalized value).
    """
    return is_array_or_tuple_with_alpha and all(PythonValidator.is_instance(c, float) and 0 <= c <= 1 for c in color)

def is_array_or_tuple_without_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 3 elements that are int values between 0
    and 255.
    """
    return PythonValidator.is_instance(color, tuple) or PythonValidator.is_instance(color, list) and len(color) == 3 and all(PythonValidator.is_instance(c, int) and 0 <= c <= 255 for c in color)

def is_array_or_tuple_with_alpha(color):
    """
    Check that the 'color' parameter is an array or a
    tuple of 4 elements that are int values between 0
    and 255.
    """
    return PythonValidator.is_instance(color, tuple) or PythonValidator.is_instance(color, list) and len(color) == 4 and all(PythonValidator.is_instance(c, int) and 0 <= c <= 255 for c in color)

def parse_rgb_color(color):
    """
    Parse the provided 'color' as RGB and returns it as
    r,g,b values.
    """
    if is_array_or_tuple_without_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255
    elif is_array_or_tuple_without_alpha(color):
        return color[0], color[1], color[2]
    else:
        raise Exception(f'The provided "color" parameter is not an RGB color.')

def parse_rgba_color(color):
    """
    Parse the provided 'color' as RGBA and returns it as
    r,g,b,a values.
    """
    if is_array_or_tuple_with_alpha_normalized(color):
        return color[0] * 255, color[1] * 255, color[2] * 255, color[3] * 255
    elif is_array_or_tuple_with_alpha(color):
        return color[0], color[1], color[2], color[3]
    else:
        raise Exception(f'The provided "color" parameter is not an RGBA color.')
