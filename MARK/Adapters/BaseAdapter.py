from Common import ResultsModel
import re

class BaseAdapter:
    # The regex stuff happens in here
    def parseOutput(self, output) -> ResultsModel:
        '''
        Receives input from a given marker and returns an ResultsModel object.
        '''
        results = ResultsModel()
        total_grade_pattern = r"Total Grade:\s*\[(\d*)\/(\d*)\]"
        res = re.search(total_grade_pattern, output)
        numerator = int(res.group(1))
        denominator = int(res.group(2))
        results.set_question_mark(numerator)
        results.set_question_worth(denominator)

        return results
