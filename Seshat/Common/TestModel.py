import Common

class TestModel:

    def __init__(self, config) -> None:

        self.prep_command = config["prep_command"]
        self.marking_command = config["marking_command"]

    def __str__(self) -> str:

        message = "This test will run the prep command: \"" + self.prep_command + "\".\n"
        message += "Then the test will run the marking command: \"" + self.marking_command + "\".\n"

        return message
