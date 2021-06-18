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

    def mark_assignments(self,  students):
        # Get list of student ids
        studentAssignments = {} # student_id-> List[assignments] (in order)
        for assignment in self.assignments: # Can be done synchronously. Only reading from config and copying folders.
            # build marker enviornment
            results = self.mark_assignment(assignment)
            # mark inside of marker
            # save assignment results separately
            # do marking via scheduler/ adapter
    def mark_assignment(self, assignment):
        # Marks the assignment.
        raise NotImplementedError
        #TODO: implement assignment marking