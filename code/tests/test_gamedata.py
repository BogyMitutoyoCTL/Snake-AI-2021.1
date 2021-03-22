import unittest

from GameData import GameData
from Field import Field
from Snake import Snake
import numpy as np


class GameDataTest(unittest.TestCase):

    def setUp(self) -> None:
        self.field: Field = Field(19, 29)
        self.snake: Snake = Snake(self.field)
        self.snake.food = (0, 0)
        self.data: GameData = self.snake.get_info()

    def tearDown(self) -> None:
        self.field = None
        self.snake = None
        self.data = None

    def test_calculated_width(self):
        """
        Regression test: we had an off-by-one error here
        """
        self.assertEqual(self.data.field.width, self.data.field_width)

    def test_calculated_height(self):
        """
        Regression test: we had an off-by-one error here
        """
        self.assertEqual(self.data.field.height, self.data.field_height)

    def test_head_is_in_middle_of_field(self):
        # Middle of 1...19: 10 = 0-based 9
        # Middle of 1...29: 15 = 0-based 14
        self.assertEqual((9, 14), (self.data.head_x, self.data.head_y))

    def test_food_distance_in_steps(self):
        # food is forced to be at (0,0), so the distance is equal to the
        # sum of the head positions (9,14)
        self.assertEqual(23, self.data.food_distance_in_steps)

    def test_food_direction_right_is_0_degrees(self):
        self.snake.food = (self.snake.head[0] + 2, self.snake.head[1])
        info = self.snake.get_info()
        self.assertEqual(0, info.food_direction)

    def test_food_direction_left_is_180_degrees(self):
        self.snake.food = (self.snake.head[0] - 4, self.snake.head[1])
        info = self.snake.get_info()
        self.assertEqual(180, info.food_direction)

    def test_food_direction_up_is_minus90_degrees(self):
        self.snake.food = (self.snake.head[0], self.snake.head[1] - 3)
        info = self.snake.get_info()
        self.assertEqual(-90, info.food_direction)

    def test_food_direction_down_is_90_degrees(self):
        self.snake.food = (self.snake.head[0], self.snake.head[1] + 4)
        info = self.snake.get_info()
        self.assertEqual(90, info.food_direction)

    def test_wall_distance(self):
        self.snake.snake[0] = (2, 3)
        info = self.snake.get_info()
        self.assertEqual(2, info.nearest_wall_distance)
        self.assertEqual(2, info.walldistance_w)
        self.assertEqual(3, info.walldistance_n)
        self.assertEqual(3, info.distance_to_wall_in_current_direction)
        self.assertEqual(25, info.walldistance_s)
        self.assertEqual(16, info.walldistance_e)

    def test_body_position(self):
        self.assertFalse(self.data.is_body(9, 13))
        self.assertTrue(self.data.is_body(9, 14))
        self.assertTrue(self.data.is_body(9, 15))
        self.assertTrue(self.data.is_body(9, 16))
        self.assertFalse(self.data.is_body(9, 17))

    def test_body_check_outside_field_does_not_throw(self):
        self.assertFalse(self.data.is_body(-1, -1))

    def test_food_position(self):
        self.assertTrue(self.data.is_food(0, 0))
        self.assertFalse(self.data.is_food(1, 0))
        self.assertFalse(self.data.is_food(0, 1))

    def test_food_outside_field_does_not_throw(self):
        self.assertFalse(self.data.is_food(-1, -1))

    def test_snake_cant_move_outside_field(self):
        self.assertFalse(self.data.can_move_to(-1, -1))

    def test_snake_cant_remain_in_place(self):
        self.assertFalse(self.data.can_move_to(self.data.head_x, self.data.head_y))

    def test_snake_cant_move_backwards(self):
        firstbodypart = self.snake.snake[1]
        self.assertFalse(self.data.can_move_to(firstbodypart[0], firstbodypart[1]))

    def test_head_position(self):
        self.assertTrue(self.data.is_head(9, 14))
        self.assertFalse(self.data.is_head(8, 14))
        self.assertFalse(self.data.is_head(10, 14))
        self.assertFalse(self.data.is_head(9, 13))
        self.assertFalse(self.data.is_head(9, 15))

    def test_head_has_age_0(self):
        self.assertEqual(0, self.data.body_age(9, 14))

    def test_snake_body_age(self):
        self.assertEqual(1, self.data.body_age(9, 15))
        self.assertEqual(2, self.data.body_age(9, 16))

    def test_non_body_age_raises_exception(self):
        with self.assertRaises(ValueError):
            self.data.body_age(9, 13)

    def test_head_view(self):
        view = self.data.head_view()
        #   YYY
        #   YNY
        #   YNY
        self.assertEqual(7, np.sum(view))
        self.assertEqual(3, np.sum(view[0]))
        self.assertEqual(2, np.sum(view[1]))
        self.assertEqual(2, np.sum(view[2]))
        self.assertFalse(view[1][1])
        self.assertFalse(view[2][1])

        self.snake.event("turn left")
        self.snake.tick()
        #  YYY
        #  YNN
        #  YYN
        data = self.snake.get_info()
        view = data.head_view()
        self.assertEqual(6, np.sum(view))
        self.assertEqual(3, np.sum(view[0]))
        self.assertEqual(1, np.sum(view[1]))
        self.assertEqual(2, np.sum(view[2]))

    def test_head_view_bits(self):
        bits = GameData.head_view_bits([[True] * 3, [True] * 3, [True] * 3])
        self.assertEqual(0b111111111, bits)
        bits = GameData.head_view_bits([[True] * 3, [False] * 3, [True] * 3])
        self.assertEqual(0b111000111, bits)
        bits = GameData.head_view_bits([[False] * 3, [False] * 3, [True] * 3])
        self.assertEqual(0b111000000, bits)
