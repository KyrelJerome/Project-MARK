import csv
import zipfile
import numpy as np
from typing import Any, Dict, List
import matplotlib.pyplot as plt
import statistics
from zipfile import ZipFile
import os
import glob
import subprocess, sys


# import pandas as pd
# from pandas.core.algorithms import mode


class Logger:

    def __init__(self, StudentModels):
        """
        Logger/Cataloguer base to receive the results of the graded assignment and organize the data.
        """
        self.StudentModels = StudentModels
        self.analyticsModel = {}
        self.csv_pathway = None

    def format_csv_header(self) -> List[str]:
        """
        Helper function for createCSV().
        Formats the header of the csv file in the following format: [UtorID, Q1, Q2, Q3,....,Qn, Final Mark],
        where n is the number of questions in the assignment.

        TO DO: self.StudentModels[0].get_results is used to find the number of items in the returned list equivalent to number of assignment questions.
        Refactor to callable variable in next iteration.
        """
        header = ['UtorID']

        for i in range(len(self.StudentModels[0].get_results())):
            questions_worth = self.StudentModels[0].get_results()[i].get_question_worth()
            header.append("Q"+str(i+1)+" Worth: "+str(questions_worth)+"/1 (in %)")

        header.append("Final Mark (in %)")

        return header

    def createCSV(self, container_path, assignment_name) -> None:
        """
        Creates a CSV file containing all student assignment marks, titled results.assignment_name.csv, and saves at given container_path location.
        Attribute self.csv_pathway value is updated with csv's pathway once csv file has been written.
        """
        csv_filename = "results."+assignment_name+".csv"

        csv_header = self.format_csv_header()
        rows = []
        for student in self.StudentModels:

            student_row = [student.get_utorid()]

            for subResult in student.get_results():
                student_row.append(subResult.get_question_mark()*100)

            student_row.append(student.get_final_mark())
            rows.append(student_row)

        # Declare full pathway
        pathway = container_path + "/" + csv_filename

        # Write to csv file found at pathway in directory
        with open(pathway, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(csv_header)
            csvwriter.writerows(rows)

        # Update class attribute self.csv_pathway
        self.csv_pathway = pathway

        print(self.csv_pathway)

    def createAnalytics(self, container_path: str, assignment_name: str, visuals: bool) -> None:
        """"
        Returns an Analytics Model of type Dict containing aggregated data

        Representation Invariants:
        - All marks are entered into student_model in 0.xx (autopct='%1.2f%%) format. Example: 89% is represented as 0.89.
        - Lengths of all Student_Models.get_results lists are equal.

        Future Implementations/Improvements:
        - Implement boundary passing mark (defaulted to 0.50 in this implementation) to a user-entered variable for flexibility.
        - Vectorize retrieval of marks from StudentModels if possible.
        - Utilize a self.number_of_questions attribute to StudentModel for assignment if implemented rather than calling a len() each time.
        """
        all_finals = []
        all_sub_results = []
        perfects = 0
        failures = 0
        zeroes = 0
        passes = 0

        # Count number of passes, failures, perfect scores and zero grades based final marks of assignment.
        for student in self.StudentModels:
            final_mark = student.get_final_mark()
            all_finals.append(final_mark)
            all_sub_results.append(student.get_results())

            if final_mark < 0.50:
                failures += 1
                if final_mark == 0.00:
                    zeroes += 1
            elif final_mark >= 0.50:
                passes += 1
                if final_mark == 1.00:
                    perfects += 1

        # Number of students with a perfect score (i.e. 100%)
        self.analyticsModel["num_perfects"] = perfects

        # Number of students who failed
        self.analyticsModel["num_failures"] = failures

        # Number of students who passed
        self.analyticsModel["num_passes"] = passes

        # Number of students receiving grade of zero
        self.analyticsModel["num_zeroes"] = zeroes

        # Calculate mean per assignment question
        num_questions = len(self.StudentModels[0].get_results())
        question_marks = []
        question_averages = {}  # Format: {Question #: Question Average}

        for i in range(num_questions):
            question_marks.append([])

        for results_list in all_sub_results:
            index = 0
            for result_model in results_list:
                question_marks[index].append(result_model.get_question_mark())
                index += 1

        for i in range(num_questions):
            question_averages["Q"+str(i+1)] = statistics.mean(question_marks[i])

        # Mean per question
        self.analyticsModel["mean_per_question"] = question_averages

        # Total Mean of Final Marks
        self.analyticsModel["total_mean"] = statistics.mean(all_finals)

        # Total Median of Final Marks
        self.analyticsModel["total_median"] = statistics.median(all_finals)

        # Mode of Final Marks
        self.analyticsModel["total_mode"] = statistics.mode(all_finals)

        if visuals:
            self.createAnalyticsVisual(assignment_name, container_path)

    def createAnalyticsVisual(self, assignment_name: str, container_path: str):
        """
        Creates visual graphs/displays of Analytic Model of assignment.
        Visuals are stored in a folder in the given container_path directory.
        HTML file is created to display all visuals in printable format in container_path/Visual_Analytics_assignment_name.html

        Requires Analytics Model to be generated (i.e. non empty)

        Visual graphs generated:
        - Figure 1 = Means per question: displays mark average per assignment question in a bar graph.
        - Figure 2 = Total, Mean, Median, Mode: displays total marks vs. frequency as well as total mean, median, mode in histogram (TO COMPLETE)
        - Figure 3 = Mark Category Proportions: displays proportion of total marks that are passes, fails, perfects scores or zeroes in a pie chart.
        """

        if self.analyticsModel == {}:
            print(
                "Analytics Model has not been generated. Cannot create Analaytics Visuals")
            return None


        visuals_folderpath = container_path+"/Analytic_ModelVisuals"
        print(visuals_folderpath)

        # Generates Figure 1.
        fig_1 = plt.figure()
        fig_1.suptitle("Figure 1: Average Marks Per Question")
        ax = fig_1.add_axes([0, 0, 1, 1])

        Qs = self.analyticsModel["mean_per_question"].keys()
        xlabels = []
        for i in Qs:
            label = "Q"+i
            xlabels.append(label)

        ylabels = self.analyticsModel["mean_per_question"].values()
        ax.bar(xlabels, ylabels)
        fig_1.show()
        fig_1.savefig(
            visuals_folderpath+"_Mean_per_Question.png")

        # Generate Figure 2
        # final_marks = []
        # for student in self.StudentModels:
        #     final_marks.append(student.get_final_mark())
        #
        # fig_2 = plt.figure()
        # final_marks.plot(kind='hist', color='whitesmoke', edgecolor='gray')
        # fig_2.xlabel('Total Marks', labelpad=15)
        # fig_2.ylabel('Frequency', labelpad=15)
        # fig_2.title(
        #     "Figure 2: Frequency of Total Marks with Total Mean, Median and Mode")
        # measurements = [self.analyticsModel["total_mean"],
        #                 self.analyticsModel["total_median"], self.analyticsModel["total_mode"]]
        # names = ["Mean", "Median", "Mode"]
        # colors = ["green", "blue", "orange"]
        #
        # for measurement, name, color in zip(measurements, names, colors):
        #     fig_2.axvline(x=measurement, linestyle='--', linewidth=2.5,
        #                   label='{0} at {1}'.format(name, measurement), c=color)
        # fig_2.legend()
        #
        # fig_2.savefig(visuals_folderpath+"Mean_per_Question.png")

        # Generate Figure 3
        fig_3 = plt.figure()
        ax = fig_3.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        descriptors = ["Passed", "Failed", "Perfect Score", "Zero Grade"]
        counts = [self.analyticsModel["num_passes"], self.analyticsModel["num_failures"],
                  self.analyticsModel["num_perfects"], self.analyticsModel["num_zeroes"]]
        ax.pie(counts, labels=descriptors, autopct='%1.2f%%')
        fig_3.savefig(
            visuals_folderpath+"_Proportions_Pie_Chart.png")

        visual_file = container_path+"/"+"Visual_Analytics_"+assignment_name+".html"

        # Write all images to HTML file visual_file
        html = open("Visual_Analytics_HTML", "x")
        message = ""

        print("html mannnneee")
        for file in glob.glob(visuals_folderpath+"/*.png"):
            print(file)
            message += f + "<img src='{file}'/><br>"

        print(message)
        html.write(message)
        html.close()

        print("html mannnneee")

        # with open(visual_file, 'w') as outputfile:
        #     outputfile.write(html)

        # Automatically open HTML file to view
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, visual_file])
        # os.startfile(visual_file)

    def get_analayticsModel(self) -> Dict:
        """
        Will return empty dictionary if analyticsModel has not been created
        """
        return self.analyticsModel

    def get_csv_pathway(self) -> str:
        """
        Will return None if csv has not been written.
        """
        return self.csv_pathway

    def giftwrap(self, receipt_dir: str, gift_dir="./") -> None:
        """
        Export CSVfile, Analytics Model and marking Receipts all in one zip folder to current directory by default.
        """

        pass

    def export_to(self, zip_name: str, objects: List[Any], pathway: str):
        """
        Exports given object/data to the given pathway in a zip folder.
        """

        with ZipFile(pathway+"/"+zip_name, 'w') as myzip:
            for object in objects:
                myzip.write(object)
        # myzip file is closed automatically
