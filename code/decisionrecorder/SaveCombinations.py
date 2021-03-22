import json
from typing import List

from decisionrecorder.Combination import Combination


class SaveCombinations:
    def __init__(self, path: str = None):
        self.path = path

    def save(self, combinations: List[Combination]):
        data = []

        for combination in combinations:
            data.append({
                "field": combination.number,
                "food": combination.food_direction,
                "decision": combination.decision})

        with open(self.path, "w+") as json_file:
            json.dump(data, json_file, indent=4)
