# Do not remove "from Algorithms import *". It's needed for reflection
from future.backports.datetime import timedelta

from Algorithms import *
from Algorithms.Algorithms import Algorithm
import gym
import pygame
import random
from datetime import datetime
import SnakeGym
from Algorithms.Algorithms import Visual
from Algorithms.RandomChoice import RandomChoice
from GameData import GameData
from RewardSystem import RewardSystem
from TrainingData import TrainingData


def all_algorithms(cls):
    """
    Finds all algorithms that are available and executable.
    :param cls: Base class (for recursive call)
    :return: List of all algorithm classes.
    """
    subclasses = [s for c in cls.__subclasses__() for s in all_algorithms(c)]
    unique_subclasses = set(cls.__subclasses__()).union(subclasses)
    unique_list = list(unique_subclasses)
    exclude_invalid = [c for c in unique_list if c.__name__ != "Visual"]
    exclude_invalid.sort(key=lambda c: c.__name__)
    return exclude_invalid


def choose_algorithm():
    algorithms = all_algorithms(Algorithm)
    for i in range(len(algorithms)):
        print(f"{i + 1}. {algorithms[i].__name__}")
    while True:
        text = input("Bitte Nummer des gewünschten Algorithmus auswählen:")
        algo = int(text)
        if 1 <= algo <= len(algorithms):
            return algorithms[algo - 1]()


def get_action_considering_epsilon(state: GameData, training_data: TrainingData, epoch: int,
                                   random_decision: Algorithm):
    # The algorithm can return 0.0 (default), so that no epsilon is applied
    epsilon = algorithm.epsilon(epoch, training_data.max_epochs)
    training_data.epsilon = epsilon
    if random.random() < epsilon:
        return random_decision.decide(state)
    else:
        return algorithm.decide(state)


def show_gui(state, epoch: int):
    global time_of_last_visualization

    visualize: bool = True
    # Nach einer bestimmten Zeit anzeigen:
    # visualize: bool = datetime.now() - time_of_last_visualization > timedelta(0, 5)
    # Alle x Epochen anzeigen:
    # visualize = epoch % 20 == 0
    if visualize:
        if not type(algorithm) is Visual:
            env.render()
        else:
            algorithm.visualize(state, env.training_data)

        pygame.time.Clock().tick(2)
        pygame.event.pump()
        time_of_last_visualization = datetime.now()


if __name__ == "__main__":
    from gym.envs.registration import register

    register(id='mitusnake-v0', entry_point='SnakeGym:SnakeEnv', )
    env: SnakeGym = gym.make("mitusnake-v0")

    training_data: TrainingData = env.training_data
    training_data.max_epochs = 10

    training_data.verbose = True

    reward_system = RewardSystem()
    reward_system.reward_eat_food = 1.0
    reward_system.reward_killed_by_wall = -0.1
    reward_system.reward_killed_by_tail = -0.2
    reward_system.reward_killed_by_starving_function = lambda steps, length: -0.1 / length
    reward_system.reward_closer_function = lambda distance: 0.05 if distance > 0 else -0.05
    env.reward = reward_system

    algorithm = choose_algorithm()
    if algorithm.reward_system is None:
        # Algorithmus hat kein Belohnungssystem
        # Er übernimmt das Belohnungssystem des Spiels
        algorithm.reward_system = reward_system
    else:
        # Algorithmus bringt das Belohnungssystem mit
        env.reward = algorithm.reward_system
    algorithm = Visual(algorithm)
    randomness_algorithm = RandomChoice()

    time_of_last_visualization = datetime.now()

    for epoch in range(training_data.max_epochs):
        env.reset()
        done = False

        while not done:
            state: GameData = env.game.get_info()
            show_gui(state, epoch)
            action = get_action_considering_epsilon(state, training_data, epoch, randomness_algorithm)
            state_before, reward, done, info = env.step(action)
            algorithm.train(state_before, action, reward)

        model, fitness = algorithm.epochfinished()

    print(training_data)
