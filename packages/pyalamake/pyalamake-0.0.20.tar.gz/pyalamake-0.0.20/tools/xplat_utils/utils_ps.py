import subprocess

from .svc import svc


# --------------------
## holds all OS process related utility functions
class UtilsPs:
    ## UT only; current UT mode
    _ut_mode = False
    ## UT only; Popen mock instance
    _ut_mock = None

    # --------------------
    ## run a process in a bash shell
    #
    # @param cmd            the bash command to run
    # @param use_raw_log    generates logging lines without a prefix; Pycharm does allow clicking on dirs
    # @param working_dir    the working directory in which to execute the cmd
    # @param log_file       where to save the output
    # @return None
    def run_process(self, cmd, use_raw_log=False, working_dir=None, log_file=None):
        svc.gbl.rc = 0
        if working_dir is None:
            working_dir = svc.utils_fs.root_dir

        proc = self._run_popen_process(cmd, working_dir)
        fp = None
        if log_file is not None:
            fp = open(log_file, 'w', encoding='utf-8', newline='\n')  # pylint: disable=consider-using-with

        lastline = ''
        lineno = 0
        while True:
            if lastline:
                if fp:
                    if use_raw_log:
                        fp.write(f'{lastline}')
                    else:
                        fp.write(f'{lineno: >3}] {lastline}')
                elif use_raw_log:
                    svc.log.raw(lastline.rstrip())
                else:
                    svc.log.output(lastline.rstrip(), lineno=lineno)
            retcode = proc.poll()
            if retcode is not None:
                break
            lastline = proc.stdout.readline()
            lineno += 1

        svc.gbl.rc = proc.returncode
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## run a cmd and returns the rc and output
    #
    # @param cmd            the bash command to run
    # @param msys2          call the command from msys2 bash shell otherwise from windows shell
    # @return tuple: (return code, a string delimited by newlines)
    def run_cmd(self, cmd, msys2=False):
        shell = True
        if msys2:
            cmd = ['c:/msys64/usr/bin/bash', '-c', cmd]
            shell = False
            # TODO move location of bash to xplat.cfg

        # TODO replace with call to _run_popen_process
        result = subprocess.run(cmd,
                                check=False,
                                shell=shell,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return result.returncode, result.stdout.rstrip()

    # --------------------
    ## run a cmd and returns the rc and output
    #
    # @param cmd            the bash command to run
    # @param working_dir    the working dir to use
    # @return proc instance from Popen
    def _run_popen_process(self, cmd, working_dir):
        if self._ut_mode:
            self.ut_mock.ut_do_call(cmd, working_dir)  # pylint: disable=no-member
            return self._ut_mock

        proc = subprocess.Popen(cmd,  # pylint: disable=consider-using-with
                                cwd=working_dir,
                                shell=True,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return proc

    # === UT functions

    # --------------------
    ## UT only;
    # @return return ut mode
    @property
    def ut_mode(self):
        return self._ut_mode

    # --------------------
    ## UT only; sets ut mode
    # @param val new ut mode
    # @return None
    @ut_mode.setter
    def ut_mode(self, val):
        ## see class instance
        self._ut_mode = val

    # --------------------
    ## UT only;
    # @return returns mock reference
    @property
    def ut_mock(self):
        return self._ut_mock

    # --------------------
    ## UT only; sets mock reference
    # @param val mock reference
    # @return None
    @ut_mock.setter
    def ut_mock(self, val):
        self._ut_mock = val
