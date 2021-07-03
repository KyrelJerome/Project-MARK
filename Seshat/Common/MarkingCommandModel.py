import Common

class MarkingCommandModel:

    def __init__(self, config) -> None:
        self.command = config["command"]
        self.timeout = config["timeout"]
        self.worth = config["worth"]



    def __str__(self) -> str:

        message = "The Marking Command: \n\t\"" + self.command + "\"\n"
        message += "It will timeout after " + str(self.timeout) + " seconds\n"
        message += "It is worth " + str(self.worth) + " of the final mark of the assignment."

        return message
