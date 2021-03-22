import unittest

from Field import Field


class FieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.field = Field(20, 30)

    def tearDown(self) -> None:
        pass

    def test_dimensions_are_reported_correctly(self) -> None:
        """
        Regression test: off-by-one error in field dimensions
        """
        self.assertEqual(30, self.field.height)
        self.assertEqual(20, self.field.width)

    def test_setPixel_only_sets_one_pixel(self) -> None:
        """
        We had some issue by lines being inserted by reference
        """
        self.field.set_pixel(1, 10, [3, 3, 3])
        self.assertEqual(self.field.field[10][1], [3, 3, 3])
        for x in range(self.field.width):
            for y in range(self.field.height):
                if x != 1 and y != 10:
                    self.assertEqual(self.field.field[y][x], [0, 0, 0])

    def test_set_pixel_outside_does_not_crash(self):
        self.field.set_pixel(-1, -1, [5, 5, 5])

    def test_field_is_equal_to_itself(self):
        self.assertTrue(self.field.is_equal(self.field))

    def test_field_is_different_to_None(self):
        self.assertFalse(self.field.is_equal(None))
