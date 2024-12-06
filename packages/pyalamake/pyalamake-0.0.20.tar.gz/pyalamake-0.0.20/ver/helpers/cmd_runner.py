import subprocess
import threading
import time

import psutil

from tools.xplat_utils.os_specific import OsSpecific
from tools.xplat_utils.utils_ps import UtilsPs
from ver.helpers import svc


# --------------------
## holds various functions to run OS processes
class CmdRunner:
    # --------------------
    ## constructor
    #
    def __init__(self):
        ## reference to the background thread running the process
        self._thread = None
        ## flag indicating if the thread is running or not
        self._finished = False

    # --------------------
    ## run a cmd and returns the rc and output
    #
    # @param cmd            the bash command to run
    # @return tuple: (return code, a string delimited by newlines)
    def run_cmd(self, cmd):
        msys2 = OsSpecific.os_name == 'win'
        ps = UtilsPs()
        rc, out = ps.run_cmd(cmd, msys2=msys2)
        return rc, out

    # --------------------
    ## stop the background running process
    #
    # @return None
    def finish(self):
        self._finished = True
        time.sleep(0.5)

    # --------------------
    ## return if the background process is running
    #
    # @return None
    def is_alive(self):
        if self._thread is None:
            return False

        return self._thread.is_alive()

    # --------------------
    ## run a task in a thread.
    #
    # run_fn has the following expected definition and behavior:
    #     def your_function(self, proc):
    #         # ... do work ...
    #
    #         # return True if you want your function to be called again
    #         # return None or False
    #         return True
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return the thread handle
    def start_task_bg(self, tag, cmd, working_dir='.'):
        self._thread = threading.Thread(target=self._runner,
                                        args=(tag, cmd, working_dir))
        self._thread.daemon = True
        self._thread.start()
        # wait for thread to start
        time.sleep(0.1)

    # === Private

    # --------------------
    ## create and start a process instance for
    # the given command line and working directory
    #
    # @param cmd         the command to execute
    # @param working_dir the working directory
    # @return the Popen process handle
    def _start_process(self, cmd, working_dir):
        proc = subprocess.Popen(cmd,  # pylint: disable=consider-using-with
                                shell=True,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                # stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=working_dir,
                                )
        return proc

    # --------------------
    ## the background thread used for running tasks. Instantiates a process and calls run_fn continually
    # until requested to stop
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return None
    def _runner(self, tag, cmd, working_dir):
        proc = self._start_task(tag, cmd, working_dir)
        while not self._finished:
            time.sleep(0.2)

        svc.log.info(f'{tag}: terminating process: "{cmd}"')
        try:
            # recursively kill any child processes
            proc2 = psutil.Process(proc.pid)
            for subproc in proc2.children(recursive=True):
                subproc.kill()
            # kill the parent
            proc.kill()
        except psutil.NoSuchProcess:
            pass

        svc.log.info(f'{tag}: process rc: {proc.returncode}')

    # --------------------
    ## starts a long running process
    # it is up to the caller to handle stdout and shutting down
    #
    # @param tag  a logging tag
    # @param cmd  the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return the Popen process handle
    def _start_task(self, tag, cmd, working_dir='.'):
        svc.log.info(f'{tag}:')
        svc.log.info(f'   cmd : {cmd}')
        svc.log.info(f'   dir : {working_dir}')

        proc = self._start_process(cmd, working_dir)
        svc.log.info(f'   pid : {proc.pid}')

        return proc
