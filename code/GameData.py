import copy
import math

from Field import Field


class GameData:
    def __init__(self):

        self.snake_length: int = 0
        self.head_x: int = 0
        self.head_y: int = 0
        self.direction: str = "north/east/south/west"  # Will be filled later
        self.walldistance_n: int = 0
        self.walldistance_e: int = 0
        self.walldistance_s: int = 0
        self.walldistance_w: int = 0
        self.food_x: int = 0
        self.food_y: int = 0
        self.field: Field = None
        self.body = []
        self.game_over = False
        self.action_space: list = None

    @property
    def last_tail_y(self):
        return self._last_tail[1]

    @property
    def last_tail_x(self):
        return self._last_tail[0]

    @property
    def _last_tail(self):
        lasttail = (-1, -1)
        maxage = -1
        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.is_body(x, y):
                    if self.body_age(x, y) > maxage:
                        maxage = self.body_age(x, y)
                        lasttail = (x, y)
        return lasttail

    @property
    def field_width(self) -> int:
        return self.walldistance_w + self.walldistance_e + 1

    @property
    def field_height(self) -> int:
        return self.walldistance_n + self.walldistance_s + 1

    @property
    def food_distance_in_steps(self) -> int:
        return abs(self.head_x - self.food_x) + abs(self.head_y - self.food_y)

    @property
    def food_direction(self) -> int:
        """
        Direction to the food in degrees.
        The orientation follows the Python rules.
        0° is right, 90° is down, 180° is left and -90° is up
        :return: Angle from head to food in degrees.
        """
        radians = math.atan2(self.food_y - self.head_y, self.food_x - self.head_x)
        return int(math.degrees(radians))

    def food_direction_closest_action(self) -> str:
        d = int(self.food_direction / 90)
        if d == 0:
            return "east"
        if d == -1:
            return "north"
        if d == 1:
            return "south"
        return "west"

    @property
    def air_line_distance(self) -> float:
        """
        Distance to the food, calculated by air-line distance.
        Note that the snake cannot walk directly. It can only walk in discrete steps.
        :return: Distance in steps, rounded to 10ths of steps
        """
        return int(10 * math.hypot(self.food_y - self.head_y, self.food_x - self.head_x)) / 10

    @property
    def nearest_wall_distance(self) -> int:
        """
        Distance to the closest wall n steps to walk.
        This will not consider the snake body.
        A wall distance of 0 is ok. It means that no more steps can be walked into the direction of the wall.
        :return: Number of steps that can be walked without crashing into a wall.
        """
        return min(self.walldistance_n,
                   self.walldistance_e,
                   self.walldistance_s,
                   self.walldistance_w)

    @property
    def distance_to_wall_in_current_direction(self) -> int:
        """
        Distance to the wall directly in front of the snake
        :return: distance in steps. 0 means that the snake should not continue walking in this direction.
        """
        return {"south": self.walldistance_s, "north": self.walldistance_n, "east": self.walldistance_e,
                "west": self.walldistance_w}[self.direction]

    def is_head(self, x: int, y: int) -> bool:
        return x == self.head_x and y == self.head_y

    def is_food(self, x: int, y: int) -> bool:
        return x == self.food_x and y == self.food_y

    def is_body(self, x: int, y: int) -> bool:
        return (x, y) in self.body

    def body_age(self, x: int, y: int) -> int:
        """
        Returns the age of a body piece of the snake.
        The older the piece, the less likely it will survive in this position.
        The head of the snake has an age of 0.
        Make sure you pass valid coordinates only. You can use is_body() to check.
        :param x: X coordinate of the body piece to get the date for.
        :param y: Y coordinate of the body piece to get the date for.
        :return: Age of the body part, 0 is the head, maximum is the length of the snake
        """
        return self.body.index((x, y))

    def can_move_to(self, x: int, y: int) -> bool:
        inside = self.field.pixel_is_inside_field(x, y)
        return inside and not self.is_body(x, y) and not self.is_head(x, y)

    def head_view(self, size: int = 3) -> list:
        """
        Returns the immediate neighborhood of the head, including the head and tail.
        The view is returned in world coordinates.
        :return:
        """
        lbound = int(-size / 2)
        ubound = int(size / 2) + 1
        surrounding = [[0 for x in range(lbound, ubound)] for y in range(lbound, ubound)]
        for dy in range(lbound, ubound):
            for dx in range(lbound, ubound):
                surrounding[dy - lbound][dx - lbound] = self.can_move_to(self.head_x + dx, self.head_y + dy)
        return surrounding

    @staticmethod
    def head_view_bits(head_view: list, size: int = 3) -> int:
        bits = 0
        lbound = int(-size / 2)
        ubound = int(size / 2) + 1
        for dy in range(lbound, ubound):
            for dx in range(lbound, ubound):
                if head_view[dy - lbound][dx - lbound]:
                    bits += 2 ** ((dy - lbound) * size + (dx - lbound))
        return bits

    def rotateClockwise(self, matrix):
        return list(zip(*matrix[::-1]))

    def absolute_to_relative(self, absolute: str) -> str:
        if absolute in ["turn left", "turn right", "straight"]:
            return absolute
        return {
            ("north", "west"): "turn left",
            ("north", "east"): "turn right",
            ("north", "north"): "straight",
            ("south", "south"): "straight",
            ("south", "west"): "turn right",
            ("south", "east"): "turn left",
            ("east", "east"): "straight",
            ("east", "north"): "turn left",
            ("east", "south"): "turn right",
            ("west", "west"): "straight",
            ("west", "north"): "turn right",
            ("west", "south"): "turn left",
        }[(self.direction, absolute)]

    def relative_to_absolute(self, relative: str) -> str:
        if relative in ["north", "east", "south", "west"]:
            return relative
        return {
            ("north", "turn left"): "west",
            ("north", "turn right"): "east",
            ("north", "straight"): "north",
            ("south", "straight"): "south",
            ("south", "turn right"): "west",
            ("south", "turn left"): "east",
            ("east", "straight"): "east",
            ("east", "turn left"): "north",
            ("east", "turn right"): "south",
            ("west", "straight"): "west",
            ("west", "turn right"): "north",
            ("west", "turn left"): "south",
        }[(self.direction, relative)]
