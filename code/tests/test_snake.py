import unittest

import numpy

from Field import Field
from Snake import Snake


class PredictableRng:
    def random(self):
        return 0.2


class SnakeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.snake = Snake(Field(5, 5), PredictableRng())

    def tearDown(self) -> None:
        pass

    def test_snake_starts_in_middle(self):
        self.assertEqual((2, 2), self.snake.head)

    def test_food_is_placed_randomly(self):
        # Due to predictable RNG, we can "guess" it
        self.assertEqual((1, 1), self.snake.food)

    def test_event_alone_does_not_move_snake(self):
        self.snake.event("north")
        self.assertEqual((2, 2), self.snake.head)

    def test_move_up_goes_north(self):
        self.snake.event("north")
        self.snake.tick()
        self.assertEqual((2, 1), self.snake.head)

    def test_move_left_goes_west(self):
        self.snake.event("west")
        self.snake.tick()
        self.assertEqual((1, 2), self.snake.head)

    def test_move_right_goes_east(self):
        self.snake.event("east")
        self.snake.tick()
        self.assertEqual((3, 2), self.snake.head)

    def test_running_into_wall_north_causes_game_over(self):
        self.snake.event("north")
        self.snake.tick()
        self.snake.tick()
        self.assertFalse(self.snake.is_game_over())
        self.snake.tick()
        self.assertTrue(self.snake.is_game_over())

    def test_running_into_wall_west_causes_game_over(self):
        self.snake.event("west")
        self.snake.tick()
        self.snake.tick()
        self.assertFalse(self.snake.is_game_over())
        self.snake.tick()
        self.assertTrue(self.snake.is_game_over())

    def test_running_into_body_causes_game_over(self):
        self.snake.snake.append((2, 4))
        self.snake.snake.append((1, 4))
        self.assertEqual(5, len(self.snake.snake))
        for move in range(4):
            self.snake.event("turn left")
            self.snake.tick()
        self.assertTrue(self.snake.is_game_over())

    def test_snake_length_4_cant_run_into_itself(self):
        # Make a length 4 snake
        self.snake.snake.append((2, 4))
        self.assertEqual(4, len(self.snake.snake))
        for move in range(4):
            self.snake.event("turn left")
            self.snake.tick()
        self.assertFalse(self.snake.is_game_over())

    def test_move_in_opposite_direction_not_possible(self):
        possible = self.snake.event("south")
        self.assertFalse(possible)

    def test_move_in_free_direction_is_possible(self):
        possible = self.snake.event("north")
        self.assertTrue(possible)

    def test_snake_becomes_longer_when_eating_food(self):
        self.snake.food = (2, 1)
        self.snake.event("north")
        self.assertEqual(3, len(self.snake.snake))
        self.snake.tick()
        self.assertEqual(4, len(self.snake.snake))

    def test_gradient_does_not_result_in_array(self):
        bodycolor = self.snake.field.field[3][2]
        green = bodycolor[1]
        self.assertNotIsInstance(green, numpy.ndarray)
        self.assertIsInstance(green, int)

