import numpy

from Snake import Snake


class RewardSystem:
    def __init__(self, verbose=False):
        self.collected_rewards = []
        self.verbose = verbose
        # rewards
        self.reward_eat_food = 1.0
        self.additional_steps_function = lambda width, height, length: (1 + length / 10) * (width + height)
        self.reward_closer_function = lambda distance: distance * 0.3
        self.reward_win = 1.0
        # penalties
        self.reward_impossible_move = -0.5
        self.reward_killed_by_wall = -1.0
        self.reward_killed_by_tail = -1.0
        self.reward_killed_by_starving_function = lambda steps, length: -0.3
        self.was_killed = False

    def clear(self):
        self.collected_rewards = [0] * 8
        self.was_killed = False

    def for_move_result(self, possible: bool) -> None:
        if not possible:
            self.collected_rewards[0] = self.reward_impossible_move
            if self.verbose:
                print("Reward system: impossible move")

    @property
    def final_reward(self) -> float:
        if self.was_killed:
            result = min(self.collected_rewards)
        else:
            #self.collected_rewards.sort()
            if abs(self.collected_rewards[0]) > abs(self.collected_rewards[-1]):
                result = self.collected_rewards[0]
            else:
                result = self.collected_rewards[-1]
        result = numpy.sum(self.collected_rewards)
        if self.verbose:
            print(f"Rewards: {self.collected_rewards} = {result}")
            print()
        return result

    def for_food_distance(self, delta_food: float) -> None:
        reward = self.reward_closer_function(delta_food)
        self.collected_rewards[1] = reward
        if self.verbose:
            print(f"Reward system: reward for distance to food = {reward}")

    def for_eating_food(self) -> None:
        self.collected_rewards[2] = (self.reward_eat_food)
        if self.verbose:
            print(f"Reward system: reward for eating food = {self.reward_eat_food}")

    def for_game_over(self, game_over_reason) -> None:
        if game_over_reason == Snake.TAILHIT:
            self.collected_rewards[3] = self.reward_killed_by_tail
            self.was_killed = True
            if self.verbose:
                print(f"Reward system: penalty being killed by tail = {self.reward_killed_by_tail}")
        if game_over_reason == Snake.WALLHIT:
            self.collected_rewards[4] = self.reward_killed_by_wall
            self.was_killed = True
            if self.verbose:
                print(f"Reward system: penalty being killed by wall = {self.reward_killed_by_wall}")
        if game_over_reason == Snake.WIN:
            self.collected_rewards[5] = self.reward_win
            if self.verbose:
                print(f"Reward system: reward for winning the game = {self.reward_win}")

    def for_starvation(self, walked: int, length: int) -> None:
        reward = self.reward_killed_by_starving_function(walked, length)
        self.collected_rewards[6] = reward
        self.was_killed = True
        if self.verbose:
            print(f"Reward system: penalty for starving = {reward}")

    def steps(self, width: int, height: int, snake_length: int) -> int:
        steps = int(self.additional_steps_function(width, height, snake_length))
        if self.verbose:
            print(f"Reward system: allow walking additional {steps} steps")
        return steps
