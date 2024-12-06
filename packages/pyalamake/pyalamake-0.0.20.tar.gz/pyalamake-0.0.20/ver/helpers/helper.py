import os
import shutil

# from pyalamake.lib.pyalamake import alamake
from pyalamake import alamake
from tools.xplat_utils.os_specific import OsSpecific
from tools.xplat_utils.utils_logger import UtilsLogger as logger
from ver.helpers import svc
from ver.helpers.cmd_runner import CmdRunner
from ver.helpers.logger_mock import Logger


# --------------------
## helper functions for verification tests
class Helper:
    makefile_path = 'out/Makefile'

    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        svc.log = Logger()
        svc.mut = alamake

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## initialize
    # any actions at the start of each test
    #
    # @param ptobj  reference to the pytest object
    # @return None
    def init_each_test(self, ptobj):
        logger.line('')
        svc.pytself = ptobj

    # --------------------
    ## terminate.
    # any actions at the end of each test
    #
    # @return None
    def term_each_test(self):
        pass

    # --------------------
    @property
    def os_name(self):
        return OsSpecific.os_name

    # --------------------
    ## run make with the given args
    #
    # @return None
    def run_make(self, args):
        crun = CmdRunner()
        cmd = f'make -f {self.makefile_path} {args}'
        return crun.run_cmd(cmd)

    # --------------------
    ## delete build directory (default: debug)
    #
    # @return None
    def del_build_dir(self):
        shutil.rmtree('debug', ignore_errors=True)

    # --------------------
    ## delete makefile
    #
    # @return None
    def del_makefile(self):
        if os.path.isfile(self.makefile_path):
            os.remove(self.makefile_path)
