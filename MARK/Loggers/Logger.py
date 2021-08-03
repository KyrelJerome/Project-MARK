# imports
import csv
import numpy as np
from typing import Any, Dict
import matplotlib.pyplot as plt
import statistics
from zipfile import ZipFile
import os
import glob


class Logger:

    def __init__(self, StudentModels: List[StudentsModel]):
        """
        Logger/Cataloguer base to receive the results model and organize data.
        """
        self.StudentModels = StudentModels
        self.analyticsModel = {}
        self.csv_pathway = None

    def format_csv_header(self) -> List[str]:
        """
        Helper function to createCSV().
        Formats the header of the csv file in the following format: [UtorID, Q1, Q2, Q3,....,Qn, Final Mark],
        where n is the number of questions in the assignment.
        """
        header = ['UtorID']

        for i in range(len(self.StudentModels[0].get_results)):
            header.append("Q"+(i+1))

        header.append("Final Mark")

        return header

    def createCSV(self, container_path, assignment_name) -> None:
        """
        Creates a CSV file of all student marks, titled results.assignment_name.csv, and saves at given container_path location.
        Attribute self.csv_pathway value is updated with csv's pathway once csv file has been written.
        """
        csv_filename = "results."+assignment_name+".csv"

        csv_header = format_csv_header()
        rows = []
        for student in self.StudentModels:
            student_row = [student.get_utorid]
            student_row.extend(student.get_results)
            student_row.extend(student.get_final_mark)
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

    def createAnalytics(self, container_path: str, assignment_name: str, visuals: bool) -> None:
        """"
        Returns an Analytics Model containing aggregated data
        R.Is:
        - All marks are entered into student_model in 0.xx format
        - Length of all list of Student_Models.get_results are all equal.

        """
        all_finals = []
        all_sub_results = []
        perfects = 0
        failures = 0
        zeroes = 0
        passes = 0

        for student in self.StudentModels:
            final_mark = student.get_final_mark()
            all_finals.append(final_mark)
            all_sub_results.append(student.sub_results)

        # TO DO: Replace "0.50" mark boundary with user-defined variable(?)
            if final_mark < 0.50:
                failures += 1
                if final_mark == 0.00:
                    zeroes += 1
            elif final_mark >= 0.50:
                passes += 1
                if final_mark == 1.00:
                    perfects += 1

        # Total Mean of Final Marks
        self.analyticsModel[total_mean] = statistics.mean(all_finals)

        # Total Median of Final Marks
        self.analyticsModel[total_median] = statistics.median(all_finals)

        # Mode of Final Marks
        self.analyticsModel[total_mode] = statistics.mode(all_finals)

        # Number of students with perfect score
        self.analyticsModel[num_perfects] = perfects

        # Number of students who failed
        self.analyticsModel[num_failures] = failures

        # Number of students who passed
        self.analyticsModel[num_passes] = passes

        # Number of students receiving grade of zero
        self.analyticsModel[num_zeroes] = zeroes

        # If we can add a self.number_of_questions attribute to StudentModel, that would be better.
        num_questions = len(self.StudentModels[0].get_results)
        question_marks = []
        question_averages = {}  # Format: {Question #: Question Average}

        for i in range(num_questions):
            question_marks.append([])

        for results_list in all_sub_results:
            index = 0
            for mark in results_list:
                question_marks[index].append(mark)
                index += 1

        for i in range(num_questions):
            question_averages["Q"+(i+1)] = statistics.mean(question_marks[i])

        # Mean per question
        self.analyticsModel[mean_per_question] = question_averages

        if visuals:
            createAnalyticsVisual(assignment_name, container_path)

    def createAnalyticsVisual(self, assignment_name: str, container_path: str):
        # Will execute based on a flag value in config (perhaps).
        # Update: will be HTML file by default.
        # IGNORE, it's a helper for another function. DO NOT CALL FROM MAIN.

        if self.analyticsModel == {}:
            print("Analytics Model has not been generated.")
            return None

        visuals_folderpath = container_path+"/AnalyticModelVisuals"

        # Generate normal distribution graph of marks

        # Generates bar graph of averages per questions (Vertical Bar Graph)
        fig_means_per_question = plt.figure()
        fig_means_per_question.add_axes([0, 0, 1, 1])

        Qs = self.analyticsModel[mean_per_question].keys()
        xlabels = []
        for i in Qs:
            label = "Q"+i
            xlabels.append(label)

        ylabels = self.analyticsModel[mean_per_question].values()
        fig_means_per_question.bar(xlabels, ylabels)
        fig_means_per_question.savefig(
            visuals_folderpath+"Mean_per_Question.png")

        # Display Mean, Median and Mode
        # number of students vs their final marks + mean median and mode using generated CSV file

        #final_marks_fig = plt.figure()
        #ax = final_marks_fig.add_subplot(1, 1, 1)

        # TO COMPLETE

        # Displays proportion of of assignment passes, fails, perfect scores and zero grades in a pie chart format.
        fig_pie = plt.figure()
        fig_pie.add_axes([0, 0, 1, 1])
        fig_pie.axis('equal')
        descriptors = ["Passed", "Failed", "Perfect Score", "Zero Grade"]
        counts = [self.analyticsModel[num_passes], self.analyticsModel[num_failures],
                  self.analyticsModel[num_perfects], self.analyticsModel[num_zeroes]]
        fig_pie(counts, labels=descriptors, autopct='%1.2f%%')
        fig_means_per_question.savefig(
            visuals_folderpath+"Proportions_Pie_Chart.png")

        visual_file = container_path+"/"+"Visual_Analytics_"+assignment_name+".html"

        # write all images to HTML file --> may need to import glob here
        html = ""
        for file in glob.glob("*.png"):  # DOUBLE CHECK EXT
            html += f"<img src='{file}'/><br>"

        with open(visual_file, 'w'):
            outputfile.write(html)

        os.startfile(visual_file)

    def get_analayticsModel(self) -> Dict:
        "Will return empty dictionary if analyticsModel has not been created"
        return self.analyticsModel

    def get_csv_pathway(self) -> str:
        """
        Will return None if csv has not been written.
        """
        return self.csv_pathway

    def giftwrap(self, receipt_pathway: str):
        """
        Call for CSV file, Analytics File, and Receipts and exports all in one zip folder, exported to gift_dir pathway.
        """
        #gift = []
        #csv = get_csv_pathway()
        #analytics = get_analyticsModel()

        # receipts

        # export_to(gift_pathway)

        pass

    def export_to(self, zip_name: str, objects: List[Any], pathway: str):
        """
        Exports given object/data to the given pathway in a zip folder.
        """

        with ZipFile(pathway+"/"+zip_name, 'w') as myzip:
            for object in objects:
                myzip.write(object)
        # myzip file is closed automatically
