import Common

class TestModel:

    def __init__(self, config) -> None:

        self.worth = config["worth"]
        self.timeout = config["timeout"]
        self.prep_command = config["prep_command"]
        self.marking_command = config["marking_command"]

    def __str__(self) -> str:

        message = "This test will run the prep command: \"" + self.prep_command + "\".\n"
        message += "Then the test will run the marking command: \"" + self.marking_command + "\" and will stop it after " + self.timeout + " seconds. It is worth " + self.worth + "of the final mark."

        return message
