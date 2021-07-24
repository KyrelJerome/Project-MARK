# Supports a tree(Soon to enable a topographically viable graph)
class ResultsModel:
    """
    Stores the results of a student's assignment or question

    ==== Attributes =====
    child_questions: (Optional) a list of ResultsModel objects for
                    subquestions of the question this ResultsModel represents
    question_notes: (Optional) Notes on the result of this question
    question_mark: The mark that the student got on the assignment/question
                   that this ResultsModel represents
    question_worth: How much the question is worth
    question_name: (Optional) The name of the question

    """

    def __init__(self):
        self.child_questions = []  # does not need to be filled
        self.question_notes = []  # does not need to be filled
        self.question_mark = 0  # must be set
        self.question_worth = None  # must be set
        self.question_name = None # does not need to be filled

    def add_result(self, child_result) -> None:
        """
        If this is empty, it is assumed that this ResultsModel 'node' doesn't have any children.
        The argument child_result is another ResultsModel
        """
        self.child_questions.append(child_result)

    def get_children(self) -> list:
        return self.child_questions

    def add_note(self, note) -> None:
        self.question_notes.append(note)

    def get_question_notes(self) -> list:
        return self.question_notes

    def set_question_mark(self, mark: float) -> None:
        self.question_mark = mark

    def get_question_mark(self) -> float:
        return self.question_mark

    def set_question_worth(self, worth: float) -> None:
        self.question_worth = worth

    def get_question_worth(self) -> float:
        return self.question_worth

    def set_question_name(self, name: str) -> None:
        """Question name is not required, without it, questions will be numbered."""
        self.question_name = name

    def get_question_name(self) -> str:
        return self.question_name

    def __str__(self) -> str:
        message = "Question name: \n\"" + self.question_name + "\"\n"
        message += "Question mark: \n\"" + self.question_mark + "\"\n"
        message += "Question worth: \n\"" + self.question_worth + "\"\n"
        return message
