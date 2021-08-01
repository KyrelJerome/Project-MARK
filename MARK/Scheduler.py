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

        self.utorids = os.listdir(self.student_submission_directory)    # TODO: This feels like a bad idea...
        self.tests = assignmentModel.tests

        self.file_name_pattern = assignmentModel.file_name_pattern

        self.student_marks_dir = self.base_dir + "/../student_marks"
        self.student_marks = [] # a list full of student_models

    def markAll(self):

        def signal_handler(signum, frame):
            raise Exception("Timed out.")

        os.mkdir(self.student_marks_dir)

        for student_utorid in self.utorids:

            # create env - making exclusive starter code.
            student_container = self.base_dir + "/" + student_utorid
            shutil.copytree(self.starter_code_directory, student_container)

            # move submissions into the said env
            for injections in self.injection_locations:
                submission_location = os.path.basename(injections)
                location_from = self.student_submission_directory + "/" + student_utorid + "/" + submission_location
                location_to = student_container + os.path.dirname(injections)
                shutil.copy(location_from, location_to)

            # Creating Student Mark Model
            student_model = Common.StudentModel.StudentModel()
            student_model.setUtorid(student_utorid) # TODO: setUtorid inside student_model

            # run the tests
            for test in self.tests:
                # running the prep commands
                os.system(test.prep_command)

                # running the marking commands
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(test.timeout)
                try:
                    output = subprocess.check_output(test.marking_command, shell=True)

                    # Adaptor
                    my_adapter = Adapters.BaseAdapter()
                    results_object = my_adapter.parseOutput(output)
                    results_object.set_question_worth(test.worth)
                    student_model.add_result(results_object) # TODO: add_result inside student_model


                except Exception as e:
                    output = "- The Marking Command \"" + str(test.marking_command) + "\" failed: [" + str(e) + "]"
                    print(output)

                    results_object = Common.ResultsModel.ResultsModel()
                    results_object.set_question_worth(test.worth)
                    student_model.add_result(results_object) # TODO: add_result inside student_model


            # Adding student results to self.student_marks
            self.student_marks.append(student_model)

            # Creating The Receipt
            self.createStudentReceipt(self, student_model, student_container)




    def createStudentReceipt(self, sm_object, container_location):

            # Creating The Receipt Body
            receipt_body = self.assignment_name + " - " + sm_object.getUtorid() + "Marking Receipt.\n" # TODO: getUtorid inside student_model
            final_mark = 0
            for resmod in sm_object.get_children():
                receipt_body += "====================\n" + resmod.get_question_name() + "\n====================\n" + resmod.get_question_notes()[0] + "\n====================\n"
                final_mark += resmod.get_question_mark() * resmod.get_question_worth()
            receipt_body += "\n\nTotal Assignment Mark: " + str(final_mark)

            # Constructing the Unique File name
            fn1 = re.sub("UTORID", sm_object.getUtorid(), self.file_name_pattern) # TODO: getUtorid inside student_model
            fn2 = re.sub("ASSIGNMENT#", self.assignment_name, fn1)
            file_name = container_location + "/" + fn2 + ".txt"

            # Creating the Receipt
            f = open( file_name , 'w' )
            f.write( receipt_body )
            f.close()


    def getAssignmentResults(self):
        return self.student_marks, self.student_marks_dir
