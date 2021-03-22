import numpy


class Field:
    """
    This is an implementation of a 2D matrix that holds RGB color values.
    It has a few convenience methods that allow better expression of the intent, compared to a pure 2D array.
    """
    BLACK = [0, 0, 0]

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.field = []
        self.field = self._generate_field(self.width, self.height)

    def set_all_pixels_to(self, color: list) -> None:
        """
        Sets all pixels of the field to the same color.
        :param color: The color to be applied to all pixels.
        :return: None. Side effect is the internal state of the field.
        """
        self.set_all_pixels_on_array(color, self.field)

    def set_all_pixels_on_array(self, color, field):
        for y in range(self.height):
            for x in range(self.width):
                field[y][x] = color

    def set_all_pixels_to_black(self) -> None:
        """
        Clears the field by setting all pixels to black.
        :return: None. Side effect is the internal state of the field.
        """
        self.set_all_pixels_to(Field.BLACK)

    def _generate_field(self, width, height) -> []:
        field = []
        for y in range(height):
            field.append([])  # empty line
            for x in range(width):
                field[y].append(Field.BLACK)
        return field

    def set_pixel(self, x: int, y: int, color: list) -> None:
        """
        Sets the color of a pixel at a defined position.
        If the position is outside of the field, nothing happens.
        :param x: X coordinate of the pixel to be changed, 0-based
        :param y: Y coordinate of the pixel to be changed, 0-based
        :param color: Color of the pixel, a list of R, G and B
        :return: None. Side effect is the internal state of the field.
        """
        if self.pixel_is_inside_field(x, y):
            self.field[y][x] = color

    def pixel_is_inside_field(self, x: int, y: int) -> bool:
        """
        Tests whether a pixel is within the boundaries of the field.
        :param x: X coordinate of the pixel to be checked, 0-based
        :param y: Y coordinate of the pixel to be checked, 0-based
        :return: True if the pixel is on the field, False if it's outside
        """
        return 0 <= y < self.height and 0 <= x < self.width

    def is_equal(self, field_to_compare: 'Field'):
        """
        Compares the pixels of this field with a reference field.
        This can be used to check whether the state has changed, e.g. for repaint decisions.
        :param field_to_compare: Reference field
        :return: True if all pixels are equal, False if one or more pixels are different.
        """
        if field_to_compare is None:
            return False
        return numpy.array_equal(field_to_compare.field, self.field)
