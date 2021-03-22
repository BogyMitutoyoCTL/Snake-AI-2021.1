from GameData import GameData
from RewardSystem import RewardSystem
from TrainingData import TrainingData
from Visualization import Visualization
from Field import Field


class Algorithm:
    def __init__(self):
        self.model = None
        self.reward_system:RewardSystem = None

    """
    This is the base class / interface for an algorithm.
    """

    def decide(self, info: GameData) -> str:
        """
        This method needs to decide for an action to be taken given the current state of the game.
        :param info: The current state of the snake game before the action is performed.
        :return: an action that is accepted by the Gym.
        """
        pass

    def epochfinished(self) -> (object, float):
        """
        When an epoch has completed, this method can be used to retrieve the model and fitness.
        :return: Tupel of model and fitness.
        The model could be a trained model in case of an AI algorithm, but could be None in case of a classic Algorithm
        """
        return None, 0.0

    def train(self, info: GameData, action, reward) -> None:
        """
        This method can be used for training / optimizing the algorithm.
        Non-learning algorithms can ignore this method.
        :param info:
        :param action: the action that has lead to the state.
        Note: when using an ɛ-approach for randomization, the action passed here is not necessarily the one last
        returned by the train() method.
        :param reward: A reward for the action.
        :return: None.
        """
        pass

    def visualize(self, data: GameData, training: TrainingData) -> Field:
        """
        Can be used to visualize the thought process of the algorithm.
        It is not needed to visualize the game state. This can be done by the Gym alone.
        :param data: the state of the game, which may be needed to calculate the visualization.
        :return: None.
        """
        pass

    def epsilon(self, epoch: int, maxepochs: int) -> float:
        """
        Calculates the randomness that shall be applied for training the algorithm.
        :param epoch: Number of the currently trained epoch
        :param maxepochs: Maximum number of epochs, the training lasts
        :return: Number between 0 and 1, representing a chance of 0% ... 100% random choice
        """
        return 0.0


class Visual(Algorithm):
    """
    This class is a default visualizer that can be used to wrap any algorithm for visualization.
    It basically delegates all methods to the algorithm passed in the constructor but paints the
    game data on its way.
    """

    def __init__(self, algorithm: Algorithm):
        super().__init__()
        self.decider: Algorithm = algorithm
        self.vis = Visualization(20, Field(10, 20))

    def decide(self, info: GameData) -> str:
        return self.decider.decide(info)

    def epochfinished(self) -> (object, float):
        return self.decider.epochfinished()

    def train(self, info: GameData, action, reward) -> None:
        return self.decider.train(info, action, reward)

    def visualize(self, data: GameData, training:TrainingData):

        layer = self.decider.visualize(data, training)
        self.vis.reset()
        self.vis.display_visualization_stats()
        self.vis.display_training(training)
        self.vis.display_game(data)
        self.vis.add_layer(layer)
        self.vis.tick()
