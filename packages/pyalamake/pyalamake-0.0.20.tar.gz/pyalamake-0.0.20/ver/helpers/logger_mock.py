from ver.helpers import svc


# --------------------
## simulates a logger instance
class Logger:
    # --------------------
    ## initialize
    def __init__(self):
        ## holds the log lines as a list; used for UT or other testing
        self.lines = []

    # --------------------
    ## clear the lines array
    #
    # @return None
    def init(self):
        self.lines = []

    # --------------------
    ## write the message to stdout and save to the array for later processing
    #
    # @param msg  the message to log
    # @return None
    def info(self, msg):
        if svc.verbose:
            print(f'INFO {msg}')
        self.lines.append(msg)
