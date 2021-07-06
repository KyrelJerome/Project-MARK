import Common
import os
import shutil

'''
    Schedules grading for a specific assignment.
    Spawns child processes to isolate risk, also de-escalating privileges when required.
'''

class Scheduler:
    def __init__(self, container_path: str, assignmentModel: Common.AssignmentModel):
        self.base_dir = container_path
        self.assignment_name = assignmentModel.name
        self.injection_locations = assignmentModel.injection_locations
        self.student_submission_directory = assignmentModel.student_submission_directory
        self.starter_code_directory = assignmentModel.starter_code_directory
        self.file_name_pattern = assignmentModel.file_name_pattern
        self.tests = assignmentModel.tests
        self.utorids = os.listdir(self.student_submission_directory)

        self.overall_result = None

    def markAll(self):

        for student in self.utorids:

            # what if student is like .DS_store or a python cache file?


            # create env - making exclusive starter code.
            student_container = self.base_dir + "/" + student
            shutil.copytree(self.starter_code_directory, student_container)

            # move submissions into the said env
            for injections in self.injection_locations:
                submission_file = os.path.basename(injections)
                location_from = self.student_submission_directory + "/" + student + "/" + submission_file
                location_to = student_container + os.path.dirname(injections)
                shutil.move(location_from, location_to)

            # run the tests
            # TODO

            # record specific results and add into the result model
            # TODO

        # make overall results model
        # TODO
