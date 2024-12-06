from dataclasses import dataclass


# --------------------
## holds singletons and global values
@dataclass
class svc:  # pylint: disable=invalid-name
    ## holds reference to Utils class
    utils = None

    ## holds reference to UtilsFs class; for file system functions
    utils_fs = None

    ## holds reference to UtilsPs class; for OS Process functions
    utils_ps = None

    ## holds reference to GenFiles class; for functions that generate specific files
    gen_files = None

    ## holds config variables
    cfg = None

    ## holds reference to logger
    log = None

    ## holds all global values
    @dataclass
    class Globals:
        ## the directory to hold output files
        outdir = 'out'
        ## holds logging tag
        tag = 'notset'
        ## holds the return code for the current operation
        rc = 0
        ## holds the overall return code for all the operations so far
        overallrc = 0
        ## indicates whether the logging should be verbose or not
        verbose = False

    ## holds reference to Globals
    gbl = Globals

    # --------------------
    ## abort the current script.
    # Note: do not use logging here since it may fail to write correctly
    #
    # @param msg  (optional) message to display
    # @return does not return
    @classmethod
    def abort(cls, msg='abort occurred, exiting'):
        import sys
        print('')
        print(f'ABRT {msg}')
        sys.stdout.flush()
        sys.stderr.flush()
        sys.exit(1)
