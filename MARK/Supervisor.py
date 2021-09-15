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
        for assignment in self.assignments:

            print("- Creating container for \"{}\".\n".format(assignment.name))

            # Creating Directory Addresses
            container_path = path + assignment.name + "-marking-container"
            receipt_path = path + "student_marks"
            analytics_path = receipt_path + "/" +"analytics"
            blanks_path = path + "blanks"

            # Creating Base Container
            if os.path.isdir(container_path):
                shutil.rmtree(container_path)
            os.mkdir(container_path)

            # Creating Marks Directory
            if os.path.isdir(receipt_path):
                shutil.rmtree(receipt_path)
            os.mkdir(receipt_path)
            os.mkdir(analytics_path)

            # Creating Blanks Directory If Necessary
            if not os.path.isdir(blanks_path):
                os.mkdir(blanks_path)


            # Handling the Scheduler
            assignment_scheduler = Scheduler(receipt_path ,blanks_path, container_path, assignment)

            print("- Starting marking sequence.\n")
            assignment_scheduler.markAll()

            print("- Supervisor receiving results from the Scheduler.\n")
            resultsList, recipts_dir_path = assignment_scheduler.getAssignmentResults()

            # Handling Logger and Cataloguer
            print("- Supervisor giving the Logger/Cataloguer the results\n")


            lc_object = Logger.Logger(resultsList)  #resultsList is a list filled with StudentModel elements
            lc_object.createCSV(analytics_path, assignment.name)
            lc_object.createAnalytics(analytics_path, assignment.name, True) # Third Parameter is the visualizer

            # PROTOTYPE: I was thinking about how it basically grabs the student marks folder that has all the receipts, grabs the csv and the anayltics and the html visualizer file, puts them in one dir and then zips them up ready to go.
            # lc_object.giftWrap(recipts_dir_path)


            print("- Supervisor has placed the following files in \""+ container_path +"\":\n")
            print("\t- \"{}\"'s CSV file\n".format(assignment.name))
            print("\t- \"{}\"'s Analytics file\n".format(assignment.name))
            print("\t- \"{}\"'s Receipt directory\n".format(assignment.name))

        if self.does_clean_flag:
            print("- \"does_clean_flag\" registered, initiating the cleaning protocol.")
            shutil.rmtree(container_path)
            print("\t- done.")
