from random import random

from GameData import GameData
from Field import Field


class BuiltInRandom:
    def random(self) -> float:
        return random()


class Snake:
    action_set = ["north", "south", "west", "east", "turn left", "turn right", "straight"]
    WALLHIT = "wallhit"
    TAILHIT = "tailhit"
    STOPPED = "stopped"
    WIN = "win"
    ONGOING = "ongoing"

    def __init__(self, rgb: Field, rng=BuiltInRandom()):
        self.field = rgb
        self.rng = rng
        self.field.set_all_pixels_to_black()
        self.game_over = False
        self.game_over_reason = Snake.ONGOING
        middle_x = int(rgb.width / 2)
        middle_y = int(rgb.height / 2)  # leave some space for the snake below
        self.snake = [(middle_x, middle_y),
                      (middle_x, middle_y + 1),  # with snake tail down
                      (middle_x, middle_y + 2)]
        self.direction = (0, -1)  # move up initially
        self.next_direction = (0, -1)
        self.food = (middle_x, 0)
        self.pixel_to_blank = None
        self.directions_rotate_right = {
            (0, -1): (1, 0),
            (1, 0): (0, 1),
            (0, 1): (-1, 0),
            (-1, 0): (0, -1)
        }
        self.directions_rotate_left = {
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
            (0, 1): (1, 0),
            (1, 0): (0, -1)
        }

        self._new_food()
        self._put_snake_on_field()

    @staticmethod
    def _add(tuple1: tuple, tuple2: tuple) -> tuple:
        return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]

    @property
    def head(self) -> tuple:
        return self.snake[0]

    def event(self, event: str) -> bool:
        if event == "north":
            direction = (0, -1)
        elif event == "west":
            direction = (-1, 0)
        elif event == "south":
            direction = (0, 1)
        elif event == "east":
            direction = (1, 0)
        elif event == "turn left":
            direction = self.directions_rotate_left[self.direction]
        elif event == "turn right":
            direction = self.directions_rotate_right[self.direction]
        elif event == "straight":
            direction = self.direction
        else:
            raise Exception("unknown move")

        added = Snake._add(self.direction, direction)
        if added != (0, 0):
            if not self.game_over:
                self.next_direction = direction
            return True
        return False

    def _move_snake_if_possible(self) -> None:
        newhead = Snake._add(self.head, self.direction)
        x = newhead[0]
        y = newhead[1]

        # Head is out of bounds
        if not 0 <= x < self.field.width:
            return self._die(Snake.WALLHIT)
        if not 0 <= y < self.field.height:
            return self._die(Snake.WALLHIT)

        # Head hits snake.
        # Consider that the last body piece will move away
        if newhead in self.snake[:-1]:
            return self._die(Snake.TAILHIT)

        # Snake didn't hit something, so head can move there
        self.snake.insert(0, newhead)

        # Head hits food
        if newhead == self.food:
            self._new_food()
        else:
            x, y = self.snake.pop()
            self.field.set_pixel(x, y, [0, 0, 0])

    def _gradient(self, value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
        in_size = in_max - in_min
        out_size = out_max - out_min
        scale_factor = out_size / in_size
        return int(out_min + (value - in_min) * scale_factor)

    def _put_snake_on_field(self) -> None:
        color_value = 0
        for x, y in self.snake:
            if color_value == 0:
                self.field.set_pixel(x, y, [0, 0, 255])  # head: blue
            else:
                green = self._gradient(color_value, 0, len(self.snake), 255, 100)
                self.field.set_pixel(x, y, [0, green, 0])  # body: green scale, encoding the past
            color_value += 1
        self.field.set_pixel(self.food[0], self.food[1], [255, 0, 0])  # apple: red

    def _new_food(self) -> None:
        food_is_on_field = False

        # Consider the end of the game
        if len(self.snake) == self.field.width * self.field.height:
            self.stop()
            return

        # Otherwise continue playing
        while not food_is_on_field:
            self.food = (int(self.rng.random() * self.field.width),
                         int(self.rng.random() * self.field.height))
            if self.food not in self.snake:
                food_is_on_field = True

    def tick(self) -> None:
        if not self.game_over:
            self.direction = self.next_direction
            self._move_snake_if_possible()
            self._put_snake_on_field()

    def stop(self) -> None:
        self._die(Snake.STOPPED)

    def is_game_over(self) -> bool:
        return self.game_over

    def get_info(self) -> GameData:
        info = GameData()
        info.snake_length = len(self.snake)
        info.head_x = self.snake[0][0]
        info.head_y = self.snake[0][1]
        info.direction = {(0, 1): "south", (0, -1): "north", (1, 0): "east", (-1, 0): "west"}[self.direction]
        info.walldistance_n = info.head_y
        info.walldistance_s = self.field.height - info.head_y - 1
        info.walldistance_w = info.head_x
        info.walldistance_e = self.field.width - info.head_x - 1
        info.food_x = self.food[0]
        info.food_y = self.food[1]
        info.field = self.field
        info.body = self.snake  # copy.deepcopy(self.snake)
        info.game_over = self.is_game_over()
        return info

    def _die(self, reason: str):
        self.game_over = True
        self.game_over_reason = reason
