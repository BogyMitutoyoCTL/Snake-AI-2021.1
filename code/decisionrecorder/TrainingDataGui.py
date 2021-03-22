import math
from tkinter import *
from typing import List

from decisionrecorder.Combination import Combination
from decisionrecorder.Configuration import Configuration
from decisionrecorder.Constants import *


class SnakeView(Frame):
    colors = {EMPTY: "white", HEAD: "blue", BLOCKED: "green", UNKNOWN: "gray"}

    def __init__(self, parent, n, direction_n):
        Frame.__init__(self, parent)

        self.n = n
        self.direction = None
        self.direction_n = direction_n
        self.size = 25

        self.board_configuration = [EMPTY] * (n * n)

        # Calculate the board margin so that the edge of the direction circle aligns with the four corners
        self.board_margin = math.sqrt(pow(((n * self.size) / 2), 2) +
                                      pow(((n * self.size) / 2), 2)) - ((n * self.size) / 2)

        self.width = n * self.size + 2 * self.board_margin
        self.height = self.width

        self.canvas = Canvas(self,
                             width=self.width,
                             height=self.height,
                             borderwidth=0,
                             highlightthickness=0)
        self.canvas.pack()

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        self.draw_direction()
        self.draw_board_tiles()
        self.draw_board_outline()

    def draw_board_tiles(self):
        for row in range(self.n):
            for column in range(self.n):
                i = row * self.n + column

                color = "purple"

                if self.board_configuration[i] in self.colors:
                    color = self.colors[self.board_configuration[i]]

                self.canvas.create_rectangle(column * self.size + self.board_margin,
                                             row * self.size + self.board_margin,
                                             (column + 1) * self.size + self.board_margin,
                                             (row + 1) * self.size + self.board_margin,
                                             fill=color, width=0)

    def draw_board_outline(self):
        # bounding rectangle
        self.canvas.create_rectangle(0 + self.board_margin,
                                     0 + self.board_margin,
                                     self.n * self.size + self.board_margin,
                                     self.n * self.size + self.board_margin,
                                     width=2)
        # vertical lines
        for i in range(self.n):
            self.canvas.create_line(i * self.size + self.board_margin,
                                    0 + self.board_margin,
                                    i * self.size + self.board_margin,
                                    self.n * self.size + self.board_margin,
                                    width=1)
        # horizontal lines
        for i in range(self.n):
            self.canvas.create_line(0 + self.board_margin,
                                    i * self.size + self.board_margin,
                                    self.n * self.size + self.board_margin,
                                    i * self.size + self.board_margin,
                                    width=1)

    def draw_direction(self):
        if self.direction is None or self.direction_n == 0:
            return

        alpha = 360 / self.direction_n

        for i in range(self.direction_n):
            color = "RosyBrown1"

            if self.direction == i:
                color = "firebrick1"

            self.canvas.create_arc(0, 0,
                                   self.width, self.height,
                                   start=-alpha * i,
                                   extent=-alpha,
                                   fill=color,
                                   outline=color)

    def set_board_configuration(self, board):
        self.board_configuration = board
        self.draw_board()

    def set_direction(self, direction):
        self.direction = direction

        self.draw_board()


class TrainingDataGui(Frame):
    def __init__(self, combinations: List[Combination] = None, configuration: Configuration = None, save_combinations = None):
        master = Tk(className="Snake training data")
        super().__init__(master)

        self.combinations = combinations
        self.configuration = configuration
        self.save_combinations = save_combinations

        self.master = master
        self.pack()

        self.frame_snake_direction = Frame(self)

        self.snake = SnakeView(self.frame_snake_direction, configuration.field_size, configuration.food_directions)
        self.button_north = Button(self.frame_snake_direction, text="North", command=self.button_north_clicked)
        self.button_south = Button(self.frame_snake_direction, text="South", command=self.button_south_clicked)
        self.button_east = Button(self.frame_snake_direction, text="East", command=self.button_east_clicked)
        self.button_west = Button(self.frame_snake_direction, text="West", command=self.button_west_clicked)
        self.button_impossible = Button(self.frame_snake_direction, text="Impossible", command=self.button_impossible_clicked)

        self.snake.grid(row=1, column=1, padx=10, pady=10)

        self.button_north.grid(row=0, column=1)
        self.button_south.grid(row=2, column=1)
        self.button_east.grid(row=1, column=2)
        self.button_west.grid(row=1, column=0)
        self.button_impossible.grid(row=2, column=2)

        self.frame_snake_direction.grid_columnconfigure(0, weight=1)
        self.frame_snake_direction.grid_rowconfigure(2, weight=1)
        self.frame_snake_direction.grid(row=0, column=0, padx=10, pady=10)

        self.frame_controls = Frame(self)
        self.button_next = Button(self.frame_controls, text="Next", command=self.button_next_clicked)
        self.button_previous = Button(self.frame_controls, text="Previous", command=self.button_previous_clicked)
        self.button_save = Button(self.frame_controls, text="Save", command=self.button_save_clicked)
        self.label_information = Label(self.frame_controls, text="10/1000")

        self.button_previous.grid(row=0, column=0, padx=10, pady=10)
        self.label_information.grid(row=0, column=1, padx=10, pady=10)
        self.button_next.grid(row=0, column=2, padx=10, pady=10)
        self.button_save.grid(row=1, column=1, padx=0, pady=0)

        self.frame_controls.grid(row=1, column=0, padx=10, pady=10)

        self.current_combination = 0
        self.load_combination(0)

    def button_north_clicked(self):
        self.set_decision_and_move_on("N")

    def button_south_clicked(self):
        self.set_decision_and_move_on("S")

    def button_east_clicked(self):
        self.set_decision_and_move_on("E")

    def button_west_clicked(self):
        self.set_decision_and_move_on("W")

    def button_impossible_clicked(self):
        self.set_decision_and_move_on("-")

    def set_decision_and_move_on(self, decision):
        self.combinations[self.current_combination].decision = decision
        self.load_combination(self.current_combination + 1)

    def button_next_clicked(self):
        self.load_combination(self.current_combination + 1)

    def button_previous_clicked(self):
        self.load_combination(self.current_combination - 1)

    def button_save_clicked(self):
        self.save_combinations.save(self.combinations)

    def load_combination(self, new_combination):
        if 0 <= new_combination < len(self.combinations):
            self.current_combination = new_combination
            combination = self.combinations[self.current_combination]

            self.snake.set_board_configuration(combination.field)
            self.snake.set_direction(combination.food_direction)

            self.label_information['text'] = str(new_combination + 1) + "/" + str(len(self.combinations))

    def show(self):
        self.mainloop()
