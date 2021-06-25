from Common import ResultsModel


class BaseAdapter:

    def parseOutput(self, output) -> ResultsModel:
        '''
        Receives input from a given marker and returns an Assignment object.
        '''
        raise NotImplementedError
