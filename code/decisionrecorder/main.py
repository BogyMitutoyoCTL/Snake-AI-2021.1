from decisionrecorder.CombinationBuilder import CombinationBuilder
from decisionrecorder.Configuration import Configuration
from decisionrecorder.SaveCombinations import SaveCombinations
from decisionrecorder.TrainingDataGui import TrainingDataGui

configuration_file = "configuration.json"
output_file = "outputNina.json"

if __name__ == "__main__":
    configuration = Configuration(configuration_file)

    builder = CombinationBuilder(configuration)

    combinations = builder.get_combinations()

    gui = TrainingDataGui(combinations=combinations,
                          configuration=configuration,
                          save_combinations=SaveCombinations(output_file))
    gui.show()
