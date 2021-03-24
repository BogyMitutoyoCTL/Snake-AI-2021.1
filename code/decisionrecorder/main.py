from decisionrecorder.CombinationBuilder import CombinationBuilder
from decisionrecorder.Configuration import Configuration
from decisionrecorder.SaveCombinations import SaveCombinations
from decisionrecorder.TrainingDataGui import TrainingDataGui

if __name__ == "__main__":
    configuration_file = "configuration.json"
    configuration = Configuration(configuration_file)

    builder = CombinationBuilder(configuration)

    combinations = builder.get_combinations()

    size = f"{configuration.field_size}x{configuration.field_size}"
    mask = f"{configuration.mask_string}"
    directions = f"{configuration.food_directions} dir"
    worker = f"{configuration.number_worker} of {configuration.number_parallel_workers}"
    output_file = f"{size} {mask}, {directions}, {worker}.json"

    gui = TrainingDataGui(combinations=combinations,
                          configuration=configuration,
                          save_combinations=SaveCombinations(output_file))
    gui.show()
