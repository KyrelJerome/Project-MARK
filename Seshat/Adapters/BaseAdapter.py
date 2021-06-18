class BaseAdapter:

    def parseOutput(self, output):
        '''
        Receives input from a given marker and returns an Assignment object.
        '''
        raise NotImplementedError
