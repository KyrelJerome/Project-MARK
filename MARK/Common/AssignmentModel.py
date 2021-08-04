from MARK.Common.FileUtility import FileUtility
import Common

class AssignmentModel:
    def __init__(self, assignment_config) -> None:

        self.name = assignment_config["name"]

        # What if this directory doesn't exist?
        self.student_submission_directory = assignment_config["student_submission_directory"]

        # what if these don't exist? or are not the files that are actually in the submissions folder?
        self.injection_locations = assignment_config["injection_locations"]
        
        # What if this directory doesn't exist?
        self.starter_code_directory = assignment_config["starter_code_directory"]

        self.file_name_pattern = assignment_config["file_name_pattern"]

        # what if this isn't a number?
        self.total_worth = assignment_config["total_worth"]

        # what if not boolean?
        self.creates_analytics_file = assignment_config["creates_analytics_file"]

        # what if not boolean?
        self.creates_csv_file = assignment_config["creates_csv_file"]

        # what if not boolean?
        self.to_percents = assignment_config["to_percents"]

        # what if it fails to create a TestModel object?
        self.tests = []
        for test_config in assignment_config["tests"]:
            self.tests.append(Common.TestModel(test_config))

        valid_student_sub_dir = FileUtility.doesFileExist(self.student_submission_directory)
        valid_injection_path = FileUtility.doesPathExist(self.injection_locations)
        valid_starter_code_dir = FileUtility.doesPathExist(self.starter_code_directory)
        # Check if required files exist
        if not valid_student_sub_dir or not valid_starter_code_dir or not valid_injection_path:
            raise FileNotFoundError("Invalid file path within configuration.")

    def __str__(self) -> str:

        message = "Assignment Name: " + self.name + "\n"
        message += "Where the student submissions are placed: \n\t\"" + self.student_submission_directory + "\"\n"
        message += "Where the starter code for this assignment is placed: \n\t\"" + self.starter_code_directory + "\"\n"
        message += "The receipts will follow the naming convention: \n\t\"" + self.file_name_pattern + "\"\n"
        message += "Total mark: " + self.total_worth + "\n"
        message += "Analyttics file will be created: " + self.creates_analytics_file + "\n"
        message += "CSV file will be created: " + self.creates_csv_file + "\n"
        message += "Final mark will be in percent: " + self.to_percents + "\n"

        message += "The test suits that are present in the assignment configuration are: \n"
        for test in self.tests:
            message += test.name + "\n"

        return message
