class LogUtility:
    '''
    Used internally to log data in a consistent manner.
    '''
    DEBUG = "DEBUG"
    VERBOSE = "VERBOSE"
    WARNING = "WARNING"
    state="DEBUG"

    @staticmethod
    def logDebug(message):
        print(message)

    @staticmethod
    def logVerbose(message):
        if LogUtility.state == LogUtility.VERBOSE:
            print(message)


