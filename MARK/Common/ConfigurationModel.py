import Common

class ConfigurationModel:

    def __init__(self, config) -> None:
        self.does_clean = config["does_clean_flag"]
        self.assignments = []
        for assignment_config in config["assignments"]:
            self.assignments.append(Common.AssignmentModel(assignment_config))

    def __str__(self) -> str:

        message = "The assignments that are present in the configuration are: \n"

        for assignment in self.assignments:
            message += assignment.name + "\n"

        message += "The system will clean after itself: " + self.does_clean + "\n"

        return message
