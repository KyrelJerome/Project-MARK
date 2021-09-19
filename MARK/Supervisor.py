from Scheduler import Scheduler
import Common
import os
import shutil
from Logger import Logger
'''
    Carries the task of building an environment for use when marking.
    Creates the folder structures required for consistent and safe marking.
'''
class Supervisor:
    def __init__(self, configuration) -> None:
        '''
        Working_path is the path for the automarkers to work from,
         a safe directory where the code has free reign.
        '''
        self.assignments = configuration.assignments
        self.does_clean_flag = configuration.does_clean

    def run(self, path):
        for assignment_object in self.assignments:

            print("- Creating container for \"{}\".\n".format(assignment_object.name))

            # Creating Directory Addresses
            container_path = path + assignment_object.name + "-marking-container"

            student_marks_path = path + assignment_object.name + "-student-marks"

            # By Default making sure not override the old student_marks.
            if os.path.isdir(student_marks_path):
                count = 1
                while os.path.isdir(student_marks_path+"-"+str(count)):
                    count+=1
                student_marks_path = student_marks_path+"-"+str(count)

            analytics_path = student_marks_path + "/analytics"
            blanks_path = path + assignment_object.name + "-blanks"

            # Creating Base Container
            if os.path.isdir(container_path):
                shutil.rmtree(container_path)
            os.mkdir(container_path)

            # Creating Marks Directory
            if os.path.isdir(student_marks_path):
                shutil.rmtree(student_marks_path)
            os.mkdir(student_marks_path)
            if assignment_object.creates_csv_file or assignment_object.creates_analytics_file:
                os.mkdir(analytics_path)

            # Creating Blanks Directory
            if os.path.isdir(blanks_path):
                shutil.rmtree(blanks_path)

            os.mkdir(blanks_path)
            injections = assignment_object.injection_locations
            for an_injection in injections:
                try:
                    shutil.copy(assignment_object.starter_code_directory + an_injection, blanks_path)
                except IOError:
                  print ("Error: Starter Code is missing \""+ an_injection +"\". Please Check the starter code provided. ")
                  return 1

            # Handling the Scheduler
            assignment_scheduler = Scheduler(student_marks_path, blanks_path, container_path, assignment_object)

            print("- Starting marking sequence.\n")
            assignment_scheduler.markAll()

            print("- Supervisor receiving results from the Scheduler.\n")
            resultsList = assignment_scheduler.getAssignmentResults()

            # Handling Logger and Cataloguer
            print("- Supervisor giving the Logger/Cataloguer the results\n")


            lc_object = Logger.Logger(resultsList)  #resultsList is a list filled with StudentModel elements

            if assignment_object.creates_csv_file:
                lc_object.createCSV(analytics_path, assignment_object.name)
            if assignment_object.creates_analytics_file:
                lc_object.createAnalytics(analytics_path, assignment_object.name, True) # Third Parameter is the visualizer

            # PROTOTYPE: I was thinking about how it basically grabs the student marks folder that has all the receipts, grabs the csv and the anayltics and the html visualizer file, puts them in one dir and then zips them up ready to go.
            # lc_object.giftWrap(student_marks_path)


            print("- Supervisor has placed the following files in \""+ container_path +"\":\n")
            print("\t- \"{}\"'s CSV file\n".format(assignment_object.name))
            print("\t- \"{}\"'s Analytics file\n".format(assignment_object.name))
            print("\t- \"{}\"'s Receipt directory\n".format(assignment_object.name))

        if self.does_clean_flag:
            print("- \"does_clean_flag\" registered, initiating the cleaning protocol.")
            shutil.rmtree(container_path)
            shutil.rmtree(blanks_path)
            print("\t- done.")
