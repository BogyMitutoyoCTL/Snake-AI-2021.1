import json

from decisionrecorder.Constants import *


class Configuration:
    mask = None
    food_directions = None
    field_size = None
    number_parallel_workers = None
    number_worker = None

    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        with open(self.path) as json_file:
            data = json.load(json_file)

            mask_string = data['mask']
            self.food_directions = data['food_directions']
            self.field_size = data['field_size']
            self.number_parallel_workers = data['number_parallel_workers']
            self.number_worker = data['number_worker']

            mask = []

            for m in mask_string:
                if m == '1':
                    mask.append(UNKNOWN)
                elif m == ' ':
                    pass
                else:
                    mask.append(EMPTY)

            self.mask = mask
