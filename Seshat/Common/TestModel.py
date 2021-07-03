import Common

class TestModel:

    def __init__(self, config) -> None:
        self.name = config["name"]

        self.prep_commands = []
        for prep_command in config["prep_commands"]:
            self.prep_commands.append(prep_command)

        self.marking_commands = []
        for marking_command in config["marking_commands"]:
            self.marking_commands.append(Common.MarkingCommandModel(marking_command))

    def __str__(self) -> str:

        message = "This test suits' name is: " + self.name + " \n"
        message += "This suite has " + str(len(self.prep_commands)) + " prep commands that need to be executed before any marking is done.\n"
        message += "After the prep commands, this suite has " + str(len(self.marking_commands)) + " marking commands that will be executed:\n"

        for marking_command in self.marking_commands:
            message += "\"" + marking_command.command + "\"\n"

        return message
