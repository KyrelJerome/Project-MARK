Common

class Util:

    def crunchTheNumbers(self, student_model):
        final_mark = 0.0
        for result in student_model.get_results():
            final_mark += resmod.get_question_mark() * resmod.get_question_worth()

        student_model.set_final_mark(final_mark)
