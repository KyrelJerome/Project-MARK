from Seshat.Common import AssignmentModel
import Common
'''
    Schedules grading for a specific assignment.
    Spawns child processes to isolate risk, also de-escalating privileges when required.
'''

class Scheduler:
    def __init__(self, assignmentModel: AssignmentModel):
        resultsLogs = []
        for runtime in AssignmentModel:
            # create fresh set if desired.
            continue
