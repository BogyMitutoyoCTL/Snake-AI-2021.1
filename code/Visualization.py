import pygame

from GameData import GameData
from TrainingData import TrainingData
from Field import Field


class Visualization:
    def __init__(self, pixel_size: int, field: Field):
        self.current_print_y: int = 0

        # PyGame stuff
        pygame.init()
        pygame.fastevent.init()
        self.clock = pygame.time.Clock()

        # Arbitrary decisions
        self._pixel_width: int = pixel_size
        self._pixel_height: int = pixel_size

        # Prepare something to show
        self.field: Field = field
        self.window = pygame.display.set_mode((field.width * pixel_size + 380, field.height * pixel_size + 40))
        pygame.display.set_caption('AI Snake @mitutoyoctlg')
        self.font_style = pygame.font.SysFont("Arial", 16)
        self.field_position: tuple = (315, 15)
        self.text_color: list = [255, 255, 255]

        # Cache
        self.last_field = None

    def tick(self) -> None:
        self.clock.tick(0)
        pygame.display.flip()

    def reset(self):
        self.current_print_y = 5

    def _draw_field(self, field: Field, offset=0):
        if self.last_field is None:
            self.last_field = Field(field.width, field.height)
            self.last_field.set_all_pixels_to([-1, -1, -1])  # ensures a repaint
            pygame.draw.rect(self.window, [50, 50, 50],
                             pygame.Rect(self.field_position[0], self.field_position[1],
                                         field.width * self._pixel_width, field.height * self._pixel_height))

        sizechange = 1 if offset > 0 else 0
        for y in range(0, field.height):
            for x in range(0, field.width):
                pixel_color = field.field[y][x]
                if offset == 0:
                    if pixel_color == self.last_field.field[y][x]:
                        continue
                left = (x - offset) * self._pixel_width + self.field_position[0] + 1 + sizechange * 5
                top = (y - offset) * self._pixel_height + self.field_position[1] + 1 + sizechange * 5
                width = self._pixel_width - 2 - sizechange * 10
                height = self._pixel_height - 2 - sizechange * 10
                pygame.draw.rect(self.window, pixel_color, pygame.Rect(left, top, width, height))

                # remember the pixel if original field
                if offset == 0:
                    self.last_field.field[y][x] = pixel_color

    def display_visualization_stats(self):
        self.text_color = [0, 255, 0]
        fps = int(self.clock.get_fps())
        self._print_in_window(f"{fps} fps")
        self._print_in_window("")

    def display_training(self, training: TrainingData):
        if training is None:
            return
        self.text_color = [0, 255, 255]
        self._print_in_window(f"Epoch: {training.epoch} / {training.max_epochs}")
        self._print_in_window(f"Steps walked: {training.number_of_steps_walked} / {training.max_number_of_steps}")
        self._print_in_window(f"↑ score (snake length): {training.best_score}")
        self._print_in_window(f"↑ steps walked: {training.best_steps_walked}")
        self._print_in_window(f"∑ training steps (all epochs): {training.total_steps_walked}")
        self._print_in_window(f"∑ food eaten (all epochs): {training.total_food_eaten}")
        self._print_in_window(f"Ø food eaten per epoch (all time): {(training.total_food_eaten / training.epoch):.2f}")
        self._print_in_window(f"Ø food eaten per epoch (moving): {training.moving_average}")
        self._print_in_window(f"ε : {int(training.epsilon * 100)}%")
        self._print_in_window("")

    def display_game(self, info: GameData):
        self.text_color = [128, 128, 255]
        self._print_in_window(f"Snake direction: {info.direction}")
        self._print_in_window(f"Snake head: {info.head_x} , {info.head_y}")
        self._print_in_window(f"Snake length (score): {info.snake_length}")
        self._print_in_window(f"")
        self._print_in_window(f"Food position: {info.food_x} , {info.food_y}")
        self._print_in_window(f"Food direction: {info.food_direction}")
        self._print_in_window(f"Distance to food in steps: {info.food_distance_in_steps}")
        self._print_in_window(f"Air-line distance to food: {info.air_line_distance}")
        self._print_in_window(f"Wall distances:")
        self._print_in_window(f"     {info.walldistance_n}")
        self._print_in_window(f"{info.walldistance_w}      {info.walldistance_e}")
        self._print_in_window(f"     {info.walldistance_s}")
        self._print_in_window(f"Distance to closest wall: {info.nearest_wall_distance}")
        self._print_in_window(f"Distance to wall in walking direction: {info.distance_to_wall_in_current_direction}")
        self._print_in_window("")
        self._draw_field(info.field)

    def _print_in_window(self, text: str) -> None:
        line_distance = 17
        self.current_print_y += line_distance
        pixels = self.font_style.render(text + "     ", True, self.text_color, [0, 0, 0])
        self.window.blit(pixels, [5, self.current_print_y])

    def add_layer(self, visualization_field):
        if visualization_field is not None:
            self._draw_field(visualization_field, 1)
