from yta_general_utils.coordinate.coordinate import Coordinate


class Region:
    """
    Class to represent a region built by two coordinates, one in
    the top left corner and another one in the bottom right 
    corner.
    """
    top_left: Coordinate = None
    bottom_right: Coordinate = None
    _width: int = None
    _height: int = None

    def __init__(self, top_left_x: int, top_left_y: int, bottom_right_x: int, bottom_right_y: int):
        self.top_left = Coordinate(top_left_x, top_left_y)
        self.bottom_right = Coordinate(bottom_right_x, bottom_right_y)
        self._width = self.bottom_right.x - self.top_left.x
        self._height = self.bottom_right.y - self.top_left.y

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def center(self):
        """
        The center position of the region represented by a tuple
        (x, y).
        """
        return self.bottom_right.x - self.width / 2, self.bottom_right.y - self.height / 2
    
