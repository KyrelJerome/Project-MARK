# Supports a tree(Soon to enable a topographically viable graph)
class ResultsModel:

    def __init__(self):
        self.child_questions = []  # does not need to be filled
        self.question_notes = []  # does not need to be filled
        self.question_mark = 100  # must be set
        self.question_worth = None  # must be set
        self.question_name = None
        self.pre_parsed = ""

    def add_result(self, child_result) -> None:
        self.child_questions.append(child_result)

    def get_children(self) -> list:
        return self.child_questions

    def add_note(self, note) -> None:
        self.question_notes.append(note)

    def get_question_notes(self) -> list:
        return self.question_notes

    def set_question_mark(self, mark) -> None:
        self.question_mark = mark

    def get_question_mark(self) -> int:
        return self.question_mark

    def set_question_worth(self, worth: int) -> None:
        self.question_worth = worth

    def get_question_worth(self) -> int:
        return self.question_worth

    def set_question_name(self, name: str) -> None:
        """Question name is not required, without it, questions will be numbered."""
        self.question_name = name

    def get_question_name(self) -> str:
        return self.question_name

    def add_pre_parsed(self, output) -> None:
        self.pre_parsed = output

    def get_pre_parsed(self) -> str:
        return self.pre_parsed

    def __str__(self) -> str:
        message = "Question name: \n\"" + self.question_name + "\"\n"
        message += "Question mark: \n\"" + self.question_mark + "\"\n"
        message += "Question worth: \n\"" + self.question_worth + "\"\n"
        return message
