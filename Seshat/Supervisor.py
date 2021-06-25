import Common
import Scheduler
class Supervisor:
    def __init__(self, configuration, working_path) -> None:
        '''
        Working_path is the path for the automarkers to work from,
         a safe directory where the code has free reign.
        '''
        self.configuration = configuration
        self.working_path = working_path
        # Set up internals based on config.
        # Shouldnt need any more data

    def run(self):
        for assignment in self.configuration:
            self.build_assignment_container(self, self.configuration.container_path)
            sched = Scheduler(assignment)
            results_list = Scheduler.compute_student_marks()

    def build_assignment_container(self, path):
        # Get list of student ids
        studentAssignments = {} # student_id-> List[assignments] (in order)
        for assignment in self.assignments: # Can be done synchronously. Only reading from config and copying folders.
            # build marker enviornment
            results = self.mark_assignment(assignment)
            # mark inside of marker
            # save assignment results separately
            # do marking via scheduler/ adapter