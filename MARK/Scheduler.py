import Common
import Adapters
import os
import shutil
import re
import signal
import Util
import subprocess

'''
    Schedules grading for a specific assignment.
    Spawns child processes to isolate risk, also de-escalating privileges when required.
'''

class Scheduler:
    def __init__(self, receipt_dir: str, blanks: str, container_path: str, assignmentModel: Common.AssignmentModel):
        self.base_dir = container_path
        self.blanks_dir = blanks
        self.receipt_dir = receipt_dir
        self.assignment_name = assignmentModel.name
        self.injection_locations = assignmentModel.injection_locations

        self.student_submission_directory = assignmentModel.student_submission_directory
        self.starter_code_directory = assignmentModel.starter_code_directory

        self.utorids = self.getUtorids(self.student_submission_directory)

        self.tests = assignmentModel.tests

        self.file_name_pattern = assignmentModel.file_name_pattern

        self.student_marks = [] # a list full of student_models

    def markAll(self):

        swissArmyKnife = Util.Util()

        def signal_handler(signum, frame):
            raise Exception("Timed out.")

        for student_utorid in self.utorids:

            # Making sure the MacOS file does not trip the marking
            if student_utorid == ".DS_Store":
                continue

            # create env - making exclusive starter code.
            student_container = self.base_dir + "/" + student_utorid
            shutil.copytree(self.starter_code_directory, student_container)
            print("- Creating Student Container: " + student_container)

            # move submissions into the said env
            for injections in self.injection_locations:
                submission_location = os.path.basename(injections)
                location_from = self.student_submission_directory + "/" + student_utorid + "/" + submission_location
                location_to = student_container + os.path.dirname(injections)

                if Common.FileUtility.doesFileExist(location_from):
                    print("- Found " + location_from)
                    shutil.copy(location_from, location_to)
                else:
                    print("- WARNING: Could not find file: " + location_from)
                    print("- Using a blank file instead.")
                    location_from_blank = self.blanks_dir + injections
                    shutil.copy(location_from_blank, location_to)



            # Creating Student Mark Model
            student_model = Common.StudentModel()
            student_model.set_utorid(student_utorid)

            anchor = os.getcwd()

            # run the tests
            print("- Running tests now for " + student_utorid)
            for test in self.tests:
                # running the prep commands
                os.system(test.prep_command)

                # running the marking commands
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(test.timeout)
                results_object = Common.ResultsModel.ResultsModel()
                os.chdir(student_container)

                # mc : marking command
                mc_output = ""
                mc_error = ""
                try:
                    output_object = subprocess.run(test.marking_command.split(), capture_output=True, encoding="utf-8")
                    mc_output = output_object.stdout
                    mc_error = output_object.stderr

                except Exception as e:
                    mc_error = "- The Marking Command \"" + str(test.marking_command) + "\" failed: [" + str(e) + "]"
                    print(mc_error)

                # Adaptor
                my_adapter = Adapters.A2_Adapter()
                results_object = my_adapter.parseOutput(mc_output, mc_error)


                results_object.set_question_name("Output of \"" + test.marking_command + "\"")
                results_object.add_note(mc_output+mc_error)
                results_object.set_question_worth(test.worth)

                student_model.add_result(results_object)

                os.chdir(anchor)


            # Calculates the Final Mark of the Student
            swissArmyKnife.crunchTheNumbers(student_model)

            # Adding student results to self.student_marks
            self.student_marks.append(student_model)

            # Creating The Receipt
            # print(student_model)
            self.createStudentReceipt(student_model, self.receipt_dir)
            print("- Finished marking " + student_utorid)



    # TODO: Maybe change the location of this method from Scheduler to either Util or Logger. Feels more appropriate if it's placed there.
    def createStudentReceipt(self, sm_object, location_of_receipt):
        print(" - Creating receipt")
        # Creating The Receipt Body
        receipt_body = self.assignment_name + " - \"" + sm_object.get_utorid() + "\" Marking Receipt.\n"
        for resmod in sm_object.get_results():
            receipt_body += "====================\n\n" + resmod.get_question_name() + "\n\n====================\n\n" + resmod.get_question_notes()[0] + "\n\n====================\n\n"

        receipt_body += "\nTotal Assignment Mark: " + str(sm_object.get_final_mark())

        # Constructing the Unique File name
        fn1 = re.sub("UTORID", sm_object.get_utorid(), self.file_name_pattern)
        fn2 = re.sub("ASSIGNMENTNAME", self.assignment_name, fn1)
        file_name = location_of_receipt + "/" + fn2

        # Creating the Receipt
        f = open( file_name , 'w' )
        f.write( receipt_body )
        f.close()

    def getUtorids(self, submissions_dir):
        if Common.FileUtility.doesDirExist(submissions_dir):
            return os.listdir(submissions_dir)
        else:
            raise FileNotFoundError("student_submission_directory: Invalid file path within configuration.")

    def getAssignmentResults(self):
        return self.student_marks
