import Common

class ConfigurationModel:
    def __init__(self, config) -> None:
        self.output_type = config.output.filename
        self.does_clean = config.output.does_clean
        self.assignments = []
        for index in range(config.assignments):
            self.assignments.append( Common.AssignmentModel(config.assignments[index]))
