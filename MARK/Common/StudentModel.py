# Supports a tree(Soon to enable a topographically viable graph)
from MARK.Common.ResultsModel import ResultsModel


class StudentModel:
    """
    Represents all information of a given student.
    Attributes
    results:List[ResultsModel]
    utorid:str
    mark:float
    """


def __init__(self):
    self.sub_results = []  # must be set
    self.final_mark = 0  # must be set
    self.utorid = None # must be set

    self.notes = []  # does not need to be filled


def add_result(self, child_result: ResultsModel) -> None:
    self.sub_results.append(child_result)

def get_results(self) -> list:
    return self.sub_results

def set_final_mark(self, mark: float) -> None:
    self.final_mark = mark

def get_final_mark(self) -> float:
    return self.final_mark

def set_utorid(self, name: str) -> None:
    self.utorid = name

def get_utorid(self) -> str:
    return self.utorid

def add_note(self, note) -> None:
    self.question_notes.append(note)

def get_question_notes(self) -> list:
    return self.question_notes

def __str__(self) -> str:
    message = "Student utorid: \n\"" + self.utorid + "\"\n"
    message += "Student final mark: \n\"" + self.final_mark + "\"\n"
    return message
