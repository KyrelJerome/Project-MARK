# Supports a tree(Soon to enable a topographically viable graph)
class ResultsModel():
    def __init__(self):
        self.child_questions = [] # does not need to be filled
        self.question_notes = [] # does not need to be filled
        self.question_mark = 100 # must be set
        self.question_worth = None # must be set
        self.question_name = None

    def add_result(self, child_result)-> None:
        self.child_questions.append(child_result)

    def set_question_worth(self, worth:int )-> None:
        self.child_questions.append()
    
    def set_question_name(self, name:str)-> None:
        """Question name is not required, without it, questions will be numbered."""
        self.question_name = name
    
    def set_question_mark(self, mark)-> None:
        self.question_mark = mark

