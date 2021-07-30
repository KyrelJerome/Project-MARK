
class Logger:

    def __init__(self, resultsModel) -> None:
        self.resultsModel = resultsModel

    def format_data_csv(self, questionCount):
        # IGNORE it's a helper for another function.
        pass

    def createAnalyticsVisual(self, analytics_model: list):
        # Will execute based on a flag value in config (perhaps).
        # Update: will be HTML file by default.
        # IGNORE, it's a helper for another function. DO NOT CALL FROM MAIN.
        pass

    def createAnalytics(self, container_path: str, assignment_name: str, visual: bool) -> None:
        """
        Creates analytics file for data aggregation, and outputs to container_path.
        Creates an analytics model based on calculations.
        """
        # CAN BE CALLED FROM SUPERVISOR
        #analytics_model = []

        # if visual:
        # createAnalyticsVisual(analytics_model)
        pass

    def createCSV(self, container_path, assignment_name) -> None:
        """
        Creates the formatted CSV file, titled results.assignment_name.csv, and outputs to container_path.
        """
        # CAN BE CALLED FROM SUPERVISOR
        pass

    def export_receipts(self, receipt_directory, receipt_file) -> None:
        """"
        Exports receipts as .txt files to zip file to receipt_directory.

        """
        # DO NOT CALL FROM SUPERVISOR

        pass

    def generate_receipts(self, receipt_directory):
        """
        Generates grade receipts for each student using result_model.
        Grade receipts are generated as .txt files, and saved in a collective receipt_file. 
        Calls helper function export_receipts() to create zip file and save receipt_file to receipt_directory
        """
        # CAN BE CALLED FROM SUPERVISOR
        pass
