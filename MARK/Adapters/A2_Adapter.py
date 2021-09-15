from Common import ResultsModel
import re

class A2_Adapter:
    # The regex stuff happens in here
    def parseOutput(self, output, error) -> ResultsModel:
        '''
        Receives input from a given marker and returns an ResultsModel object.
        '''
        results = ResultsModel.ResultsModel()

        # if error:
        #     results.set_question_mark(0)
        # else:

        # mark = 0
        total = 0

        tags_to_check_for = ["Insert Tests total : ", "Delete Tests total : ", "Contains Tests total : ", "Sort Tests total : ", "Merge Tests total : ", "Auto-Complete Tests total : ", "Auto-Correct Tests total : "]
        weights = [0.1, 0.15, 0.1, 0.2, 0.15, 0.1, 0.2]

        for i in range(len(tags_to_check_for)):
            tmp_mark, tmp_total = self.check_test(tags_to_check_for[i], output, error)

            # print(tmp_mark, tmp_total)
            total += (tmp_mark/tmp_total)*weights[i] # this gets multiplied by 100 later
            # print(total)
            # mark += tmp_mark
            # total += tmp_total


        results.set_question_mark(total)

        return results


    def check_test(self, specific_tag, output, error):

        grade_pattern = r""+specific_tag+"(\d*)\/(\d*)"
        res = re.search(grade_pattern, output)

        # print(res)

        if res == None:
            if specific_tag == "Insert Tests total : ":
                return 0, 8
            if specific_tag == "Merge Tests total : ":
                return 0, 5
            if specific_tag == "Contains Tests total : ":
                return 0, 7
            if specific_tag == "Delete Tests total : ":
                return 0, 9
            if specific_tag == "Auto-Complete Tests total : ":
                return 0, 8
            if specific_tag == "Auto-Correct Tests total : ":
                return 0, 11
            if specific_tag == "Sort Tests total : ":
                return 0, 10

        else:

            numerator = float(res.group(1))
            denominator = float(res.group(2))

            return numerator, denominator
