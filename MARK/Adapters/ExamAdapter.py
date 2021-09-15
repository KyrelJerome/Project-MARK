from Common import ResultsModel
import re

class ExamAdapter:
    # The regex stuff happens in here
    def parseOutput(self, output) -> ResultsModel:
                '''
                Receives input from a given marker and returns an ResultsModel object.
                FOR EXAM!
                '''
                results = ResultsModel.ResultsModel()


                total_grade_pattern_BOTH = r"FAILED \(failures=(\d*), errors=(\d*)\)"
                total_grade_pattern_FAILURE = r"FAILED \(failures=(\d*)\)"
                total_grade_pattern_ERROR = r"FAILED \(errors=(\d*)\)"

                number_of_tests_pattern = r"Ran (\d*) tests in"


                res_NUM = re.search(number_of_tests_pattern, output)
                res_BOTH = re.search(total_grade_pattern_BOTH, output)
                res_FAILURE = re.search(total_grade_pattern_FAILURE, output)
                res_ERROR = re.search(total_grade_pattern_ERROR, output)


                num_failures = 0
                num_errors = 0
                number_of_tests = 0

                if res_NUM:
                    number_of_tests = float(res_NUM.group(1))
                else:
                    number_of_tests = 1

                if res_BOTH:
                    num_failures = float(res_BOTH.group(1))
                    num_errors = float(res_BOTH.group(2))
                elif res_FAILURE:
                    num_failures = float(res_FAILURE.group(1))
                elif res_ERROR:
                    num_errors = float(res_ERROR.group(1))


                numerator = number_of_tests - (num_failures + num_errors)
                denominator = number_of_tests

                results.set_question_mark(numerator/denominator)

                return results
