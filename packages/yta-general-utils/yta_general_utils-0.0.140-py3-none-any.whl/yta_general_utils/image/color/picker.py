from yta_general_utils.region import PixelFilterFunction
from yta_general_utils.image.parser import ImageParser
from collections import Counter
from PIL import Image
from typing import Union

import numpy as np


class ColorPicker:
    """
    Class to encapsulate and simplify the functionality related to
    image color detection.
    """
    @staticmethod
    def get_most_common_green_rgb_color(image: Union[str, Image.Image, np.ndarray]):
        """
        Returns the most common (dominant) rgb color in a 
        (r, g, b) format.
        """
        image = ImageParser.to_pillow(image)

        return ColorPicker.get_dominant_color(image, PixelFilterFunction.is_green)

    @staticmethod
    def get_most_common_green_rgb_color_and_similars(image: Union[str, Image.Image, np.ndarray]):
        """
        Returns the most common rgb color and its similar colors
        found in the provided 'image_filename' as a pair of values
        (most_common, similars). Extract them as a pair.
        """
        image = ImageParser.to_pillow(image)

        return ColorPicker.get_dominant_and_similar_colors(image, PixelFilterFunction.is_green, _is_similar_green)

    @staticmethod
    def get_dominant_color(image: Union[str, Image.Image, np.ndarray], pixel_filter_function: PixelFilterFunction = None):
        """
        Opens the provided 'image_filename' and gets the dominant
        color applying the 'pixel_filter_function' if provided.
        """
        image = ImageParser.to_pillow(image)

        dominant, _ = _get_dominant_color(image, pixel_filter_function)

        return dominant

    @staticmethod
    def get_dominant_and_similar_colors(image: Union[str, Image.Image, np.ndarray], pixel_filter_function: PixelFilterFunction = None, similarity_function = None):
        """
        Opens the provided 'image_filename', gets the dominant
        color and also the similar ones by applying the 
        'pixel_filter_function' if provided.
        """
        image = ImageParser.to_pillow(image)

        return _get_dominant_color(image, pixel_filter_function, similarity_function)



def _is_similar_green(color1, color2, tolerance: float = 30):
    if not tolerance:
        tolerance = 30

    # TODO: This below should be comparing 
    return (abs(color1[0] - color2[0]) <= tolerance * 0.5 and
            abs(color1[1] - color2[1]) <= tolerance * 2 and
            abs(color1[2] - color2[2]) <= tolerance * 0.5)

def _get_dominant_color(image: Union[str, Image.Image, np.ndarray], pixel_filter_function: PixelFilterFunction = None, similarity_function = None):
    image = ImageParser.to_pillow(image)
    
    pixels = list(image.getdata())
    if pixel_filter_function is not None:
        pixels = [pixel for pixel in pixels if pixel_filter_function(pixel)]

    color_count = Counter(pixels)

    if not color_count:
        return None, None

    dominant_color = color_count.most_common(1)[0][0] #[0][1] is the 'times'

    if similarity_function is None:
        return dominant_color, None

    similar_colors = [color for color in color_count.keys() if similarity_function(color, dominant_color, 30) and color != dominant_color]
    
    return dominant_color, similar_colors

# TODO: Maybe make this methods work with numpy arrays (?)