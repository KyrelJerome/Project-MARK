import Common
import Scheduler
import os
import shutil

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

            container_path = path + assignment.name + "-marking-container"
            os.mkdir(container_path)

            assignment_scheduler = Scheduler(container_path, assignment)

            print("- Starting marking sequence.\n")
            assignment_scheduler.markAll()

            print("- Supervisor receiving results from the Scheduler.\n")
            resultsModel, recipts_dir_path = assignment_scheduler.getAssignmentResults()

            print("- Supervisor giving the Logger/Cataloguer the results\n")
            lc_box = Loggers.textLoggerCatalogur(resultsModel)

            # parameter tells the method where to save the CSV and with what name, it also retuns the path of the said csv
            csv_path = lc_box.createCSV(container_path, assignment.name)
            # parameter tells the method where to save the analytics and with what name, it also retuns the path of the said analytics
            analytics_path = lc_box.createAnalytics(container_path, assignment.name)


            print("- Supervisor has placed the following files in the mentioned path:\n")
            print("\t- \"{}\"'s CSV file: \"{}\"\n".format(assignment.name, csv_path))
            print("\t- \"{}\"'s Analytics file: \"{}\"\n".format(assignment.name, analytics_path))
            print("\t- \"{}\"'s Receipt directory: \"{}\"\n".format(assignment.name, recipts_dir_path))

        if self.does_clean_flag:
            print("- \"does_clean_flag\" registered, initiating the cleaning protocol.")
            shutil.rmtree(container_path)
            print("\t- done.")
