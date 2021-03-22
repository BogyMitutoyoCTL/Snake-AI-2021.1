import unittest

import gym
import numpy

import SnakeGym
from TrainingData import TrainingData


class SnakeTest(unittest.TestCase):
    def setUp(self) -> None:
        from gym.envs.registration import register
        try:
            register(id='mitusnake-v0', entry_point='SnakeGym:SnakeEnv', )
        except gym.error.Error:
            # can't register multiple times
            pass
        self.env: SnakeGym = gym.make("mitusnake-v0")
        self.trainingdata: TrainingData = self.env.training_data

    def tearDown(self) -> None:
        pass

    def test_gym_is_not_reset_in_constructor(self):
        # these indirect observations can tell whether the env was reset
        self.assertEqual(0, self.trainingdata.epoch)
        self.assertEqual(0, self.env.last_distance)
        self.assertEqual(0, self.trainingdata.max_number_of_steps)

    def test_action_space(self):
        self.assertEqual(7, self.env.action_space.n)

    def test_reset_returns_observation(self):
        self.assertIsNotNone(self.env.reset())

    def test_reset_has_snake_on_field(self):
        observation = self.env.reset()
        self.assertNotEqual(0, numpy.sum(observation))

    def test_step_gives_reward(self):
        self.env.reset()
        self.env.reward.reward_impossible_move = -100
        state, reward, done, _ = self.env.step("south")
        self.assertTrue(reward<0)

