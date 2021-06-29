from Common import ResultsModel
from Adapters import BaseAdapter

class JsonAdapter(BaseAdapter):

    def parseOutput(self, output) -> ResultsModel:
        '''
        Receives input as Json a given marker and returns an Assignment object.
        '''
        raise NotImplementedError
