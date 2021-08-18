from Common import ResultsModel
import re

class Test2Adapter:
    # The regex stuff happens in here
    def parseOutput(self, output) -> ResultsModel:
        '''
        Receives input from a given marker and returns an ResultsModel object.
        FOR TEST2Q2 ONLY!
        '''
        results = ResultsModel.ResultsModel()

        # total_grade_pattern_GREEN = r"OK"
        total_grade_pattern_BOTH = r"FAILED \(failures=(\d*), errors=(\d*)\)"
        total_grade_pattern_FAILURE = r"FAILED \(failures=(\d*)\)"
        total_grade_pattern_ERROR = r"FAILED \(errors=(\d*)\)"

        # print(output)

        # res_GREEN = re.search(total_grade_pattern_GREEN, output)
        res_BOTH = re.search(total_grade_pattern_BOTH, output)
        res_FAILURE = re.search(total_grade_pattern_FAILURE, output)
        res_ERROR = re.search(total_grade_pattern_ERROR, output)

        num_failures = 0
        num_errors = 0

        if res_BOTH:
            num_failures = float(res_BOTH.group(1))
            num_errors = float(res_BOTH.group(2))
        elif res_FAILURE:
            num_failures = float(res_FAILURE.group(1))
        elif res_ERROR:
            num_errors = float(res_ERROR.group(1))

        numerator = 3 - (num_failures + num_errors)
        denominator = 3

        # print(numerator,denominator)
        results.set_question_mark(numerator/denominator)

        return results
