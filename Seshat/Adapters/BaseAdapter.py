from Common import ResultsModel


class BaseAdapter:
    # The regex stuff happens in here
    def parseOutput(self, output) -> ResultsModel:
        '''
        Receives input from a given marker and returns an Assignment object.
        '''
        raise NotImplementedError
