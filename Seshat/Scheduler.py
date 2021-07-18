import Common
import Adapters
import os
import shutil
import re
import signal

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

        self.utorids = os.listdir(self.student_submission_directory)
        self.tests = assignmentModel.tests

        self.file_name_pattern = assignmentModel.file_name_pattern

        self.student_marks = [] # a list full of ResultModels

    def markAll(self):

        def signal_handler(signum, frame):
            raise Exception("Timed out.")

        for student in self.utorids:

            # what if student is like .DS_store or a python cache file?
            # TODO

            # create env - making exclusive starter code.
            student_container = self.base_dir + "/" + student
            shutil.copytree(self.starter_code_directory, student_container)

            # move submissions into the said env
            for injections in self.injection_locations:
                submission_location = os.path.basename(injections)
                location_from = self.student_submission_directory + "/" + student + "/" + submission_location
                location_to = student_container + os.path.dirname(injections)
                shutil.copy(location_from, location_to)

            test_results = []

            # run the tests
            for test in self.tests:
                # running the prep commands
                os.system(test.prep_command)

                # running the marking commands
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(60)
                try:
                    output = subprocess.check_output(test.marking_command, shell=True)

                    my_adapter = Adapters.BaseAdapter()
                    results_object = my_adapter.parseOutput(output)

                    test_results.append(results_object)

                    # TODO: create a Receipt and inject output into it
                    # make sure to follow the convention mentioned in the
                    # config file.

                except Exception as e:
                    print("- The Marking Command \"{}\" failed: [{}]".format(test.marking_command, e))


            # TODO: Add up the results of all ResultModels (in test_results)
            # and create a *Super* ResultModel object that contains the final
            # mark of this student given ALL tests


            # Assuming this is the variable that holds the student final result
            student_mark = #EXAMPLEOBJECT


            self.student_marks.append(student_mark)


    def getAssignmentResults():
        # Is this a good idea? I'm returning a list full of ResultModels as the first thing

        return self.student_marks,
