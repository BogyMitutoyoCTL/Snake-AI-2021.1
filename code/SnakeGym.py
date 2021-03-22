import copy

import gym
import numpy
import pygame
from gym import spaces

from GameData import GameData
from RewardSystem import RewardSystem
from TrainingData import TrainingData
from Visualization import Visualization
from Field import Field
from Snake import Snake


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    width = 10
    height = 20

    def __init__(self):
        self.is_render_initialized = False
        self.observation_space = spaces.Box(low=0, high=255, shape=[self.height, self.width, 3], dtype=numpy.int)
        self.action_space = spaces.Discrete(7)

        self.renderer: Visualization = None
        self.game: Snake = None
        self.last_distance = 0
        self.training_data: TrainingData = TrainingData()
        self.reward: RewardSystem = RewardSystem(verbose=False)

    def _render_initialize(self) -> None:
        self.renderer = Visualization(20, self.game.field)
        self.renderer.reset()
        self.is_render_initialized = True

    def step(self, action) -> (GameData, float, bool, set):
        if type(action) is not str:
            action = Snake.action_set[action]

        self.reward.clear()

        state_before_move: GameData = copy.deepcopy(self.game.get_info())
        #state_before_move=self.game.get_info()
        move_was_possible = self.game.event(action)
        self.reward.for_move_result(move_was_possible)

        self.game.tick()
        state_after_move: GameData = self.game.get_info()
        self.training_data.walk_step()

        self.last_distance = state_before_move.air_line_distance
        delta_food: float = self.last_distance - state_after_move.air_line_distance
        self.reward.for_food_distance(delta_food)

        if state_after_move.snake_length - self.training_data.last_score > 0:
            self.reward.for_eating_food()
            self.training_data.max_number_of_steps += self.reward.steps(self.width, self.height, state_after_move.snake_length)
            self.training_data.score(state_after_move.snake_length)

        if self.game.is_game_over():
            self.reward.for_game_over(self.game.game_over_reason)

        if self.training_data.steps_exceeded():
            self.reward.for_starvation(self.training_data.number_of_steps_walked, state_after_move.snake_length)

        done = self.game.is_game_over() or self.training_data.steps_exceeded()
        state_before_move.game_over = done
        return state_before_move, self.reward.final_reward, done, {}

    def reset(self) -> GameData:
        self.game = Snake(Field(self.width, self.height))
        self.last_distance = self.game.get_info().air_line_distance
        if self.is_render_initialized:
            self.renderer.reset()

        self.training_data.next_epoch()
        self.training_data.max_number_of_steps = 3* self.reward.steps(self.width, self.height, len(self.game.snake))

        return self.game.get_info()

    def render(self, mode='human', close=False) -> None:
        if not self.is_render_initialized:
            self._render_initialize()
        self.renderer.reset()
        self.renderer.display_visualization_stats()
        info = self.game.get_info()
        self.renderer.display_training(self.training_data)
        self.renderer.display_game(info)
        self.renderer.tick()
        pygame.event.pump()
