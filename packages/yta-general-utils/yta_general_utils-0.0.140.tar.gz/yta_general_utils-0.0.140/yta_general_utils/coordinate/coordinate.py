from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_general_utils.random import random_int_between
from yta_general_utils.math import Math

import numpy as np


NORMALIZATION_MIN_VALUE = -10000
"""
The lower limit for the normalization process.
"""
NORMALIZATION_MAX_VALUE = 10000
"""
The upper limit for the normalization process.
"""

class CoordinateType(Enum):
    """
    Enum class to represent a coordinate type that 
    defines the way to make the calculations.
    """
    CORNER = 'corner'
    """
    The type of coordinate that represents the upper
    left corner of the object that uses the coordinate
    with this type.
    """
    CENTER = 'center'
    """
    The type of coordinate that represents the center of
    the object that uses the coordinate with this type.
    """

class Coordinate:
    """
    Class to represent a coordinate point ('x', 'y').
    """
    position: tuple = None
    """
    The ('x', 'y') tuple containing the position
    coordinate.
    """
    _is_normalized: bool = False
    """
    Internal function to know if it has been normalized
    or not.
    """

    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]
    
    @property
    def is_normalized(self):
        return self._is_normalized

    def __init__(self, x: float, y: float, is_normalized: bool = False):
        if not NumberValidator.is_number_between(x, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(y, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE):
            raise Exception(f'The "x" and "y" parameters must be values between {str(NORMALIZATION_MIN_VALUE)} and {str(NORMALIZATION_MAX_VALUE)} and "{str(x)}, {str(y)}" provided.')
        
        if not PythonValidator.is_boolean(is_normalized):
            raise Exception('The "is_normalized" parameter must be a boolean value.')
        
        self.position = (x, y)
        self._is_normalized = is_normalized

    def get_x(self):
        """
        Return the 'x' value.
        """
        return self.x
    
    def get_y(self):
        """
        Return the 'y' value.
        """
        return self.y

    def as_tuple(self):
        """
        Return the coordinate as a tuple ('x', 'y').
        """
        return Coordinate.to_tuple(self)
    
    def as_array(self):
        """
        Return the coordinate as an array ['x', 'y'].
        """
        return Coordinate.to_array(self)

    def normalize(self):
        """
        Normalize the coordinate by turning the values into
        a range between [0.0, 1.0]. This will be done if the
        values have not been normalized previously.
        """
        if not self._is_normalized:
            self.position = Coordinate.normalize_tuple(self.position)
            self._is_normalized = True

        return self

    def denormalize(self):
        """
        Denormalize the coordinate values by turning them
        from normalized values to the real ones. This will
        be done if the values have been normalized 
        previously.
        """
        if self._is_normalized:
            self.position = Coordinate.denormalize_tuple(self.position)
            self._is_normalized = False

        return self

    @staticmethod
    def to_tuple(coordinate):
        """
        Turn the provided 'coordinate' to a tuple like ('x', 'y').
        """
        return coordinate.position
    
    @staticmethod
    def to_array(coordinate):
        """
        Turn the provided 'coordinate' to an array like ['x', 'y'].
        """
        return [coordinate.x, coordinate.y]

    @staticmethod
    def generate(amount: int = 1):
        """
        Generate 'amount' coordinates with random values
        between [0, 1920] for the 'x' and [0, 1080] for
        the 'y', that are returned as an array of instances.

        The 'amount' parameter is limited to the interval 
        [1, 100].
        """
        if not NumberValidator.is_number_between(amount, 1, 100):
            raise Exception(f'The provided "amount" parameter "{str(amount)}" is not a number between 1 and 100.')
        
        return Coordinate(random_int_between(0, 1920), random_int_between(0, 1080))
    
    @staticmethod
    def to_numpy(coordinates: list['Coordinate']):
        """
        Convert a list of Coordinates 'coordinates' to
        numpy array to be able to work with them.

        This method does the next operation:
        np.array([[coord.x, coord.y] for coord in coordinates])
        """
        if not PythonValidator.is_list(coordinates):
            if not PythonValidator.is_instance(coordinates, Coordinate):
                raise Exception('The provided "coordinates" parameter is not a list of NormalizedCoordinates nor a single NormalizedCoordinate instance.')
            else:
                coordinates = [coordinates]
        elif any(not PythonValidator.is_instance(coordinate, Coordinate) for coordinate in coordinates):
            raise Exception('At least one of the provided "coordinates" is not a NormalizedCoordinate instance.')

        return np.array([coordinate.as_array() for coordinate in coordinates])
    
    @staticmethod
    def normalize_tuple(coordinate: tuple):
        """
        Normalize the provided 'coordinate' by applying
        our normalization limits. This means turning the
        non-normalized 'coordinate' to a normalized one
        (values between 0.0 and 1.0).
        """
        return (
            Math.normalize(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE),
            Math.normalize(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)
        )
    
    @staticmethod
    def denormalize_tuple(coordinate: tuple):
        """
        Denormalize the provided 'coordinate' by applying
        our normalization limits. This means turning the 
        normalized 'coordinate' (values between 0.0 and
        1.0) to the not-normalized ones according to our
        normalization limits.
        """
        return (
            Math.denormalize(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE),
            Math.denormalize(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)
        )
    
    @staticmethod
    def is_valid(coordinate: tuple):
        """
        Check if the provided 'coordinate' is valid or not.
        A valid coordinate is a tuple with two elements that
        are values between our normalization limits.
        """
        if not PythonValidator.is_instance(coordinate, 'Coordinate') and (not PythonValidator.is_tuple(coordinate) or len(coordinate) != 2 or not NumberValidator.is_number_between(coordinate[0], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE) or not NumberValidator.is_number_between(coordinate[1], NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)):
            return False
        
        return True

    @staticmethod
    def validate(coordinate: tuple, parameter_name: str):
        """
        Validate if the provided 'coordinate' is a coordinate
        with values between our normalization limits.
        """
        if not Coordinate.is_valid(coordinate):
            raise Exception(f'The provided "{parameter_name}" parameter is not a valid tuple of 2 elements that are values between our limits {str(NORMALIZATION_MIN_VALUE)} and {str(NORMALIZATION_MAX_VALUE)}. Please, provide a valid coordinate.')