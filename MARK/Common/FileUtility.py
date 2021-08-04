import os

class FileUtility:
    '''
    Performs tasks interacting with files on the local filesystem.
    '''
    @staticmethod
    def doesFileExist(path:str)->bool:
        '''
        Returns true if a file exists
        '''
        return os.path.exists(path) and os.path.isfile(path)

    @staticmethod
    def doesPathExist(path:str)-> bool:
        '''
        Returns true if a path exists
        '''
        return os.path.exists(path)

    @staticmethod
    def doesDirExist(path:str)->bool:
        '''
        Returns true if a file exists
        '''
        return os.path.exists(path) and os.path.isdir(path)
