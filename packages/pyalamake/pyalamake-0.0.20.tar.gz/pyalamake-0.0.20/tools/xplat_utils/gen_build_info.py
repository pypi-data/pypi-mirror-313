import os
import re
import sys

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## generates the build_info information
class GenBuildInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## the file pointer for the build_info file
        self._fp = None
        ## the path to the build_info file
        self._path = None
        ## the overall exit return code
        self._exitrc = 0

    # --------------------
    ## generate build_info file
    #
    # @param subdir  (optional) subdirectory to place the constants files
    # @return None
    def run(self, subdir):
        if svc.cfg.mod_tech in ['', 'python']:
            self.gen_build_info(subdir, 'build_info.py')
        elif svc.cfg.mod_tech in ['cpp', 'arduino']:
            self.gen_build_info(subdir, 'build_info.txt')
        else:
            svc.log.warn(f'gen_build_info: does not work for tech: {svc.cfg.mod_tech}')
            svc.gbl.rc = 1

    # --------------------
    ## generate the build_info.py file in the module/app directory
    #
    # @param subdir   the subdirectory in the source root directory
    # @param fname    the build_info filename to use
    # @return None
    def gen_build_info(self, subdir, fname):
        if subdir:
            filedir = os.path.join('lib', subdir)
        else:
            filedir = os.path.join('lib')

        if svc.cfg.is_module:
            mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
            if not os.path.isdir(mod_dir):
                svc.log.warn(f'gen_build_info: dir does not exist: {mod_dir}')
                svc.gbl.rc = 1
                return

            path = os.path.join(str(mod_dir), filedir)
        else:
            path = os.path.join(svc.utils_fs.root_dir, filedir)

        path = os.path.join(path, fname)
        # svc.log.dbg(f'path: {path}')

        # generate file
        self.init(path)
        svc.gbl.rc = self.gen(svc.cfg.version)
        self.term()

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        msg = f'gen: {fname} rc={svc.gbl.rc}'
        if not svc.gbl.verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## initialize
    #
    # @param path     the path to the build_info file
    # @return None
    def init(self, path):
        self._path = path

        self._fp = open(self._path, 'w', encoding='utf-8', newline='\n')  # pylint: disable=consider-using-with

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._fp is not None:
            self._fp.close()

    # --------------------
    ## generate all build info
    #
    # @param version   the module/app version
    # @return error return code
    def gen(self, version):
        self._gen_init(version)
        self._gen_git_sha()
        self._gen_git_branch()
        self._gen_uncommitted_changes()
        self._gen_unpushed_commits()
        if svc.cfg.mod_tech != 'python':
            self._writeln('    === */')

        return self._exitrc

    # --------------------
    ## generate common build values
    #
    # @param version   the module/app version
    # @return None
    def _gen_init(self, version):
        if svc.cfg.mod_tech == 'python':
            self._writeln('class BuildInfo:  # pylint: disable=too-few-public-methods')
        else:
            self._writeln('/* === Build Info:')

        m = re.search(r'^(\d+\.\d+\.\d+) ', sys.version)
        self._set('python version', 'python_version', m.group(1))
        self._set('OS name', 'os_name', f'{os.name}:{OsSpecific.os_name}')

        # ensure file is created & flushed here so the import works cleanly
        self._fp.flush()

        self._set('version', 'version', version)

    # --------------------
    ## set the value in BuildInfo object
    #
    # @param tag    tag for logging
    # @param name   the name of the variable
    # @param val    the value of the variable
    # @return None
    def _set(self, tag, name, val):
        if svc.gbl.verbose:
            svc.log.ok(f'{tag: <25}: {val}')
        self._writeln(f'    {name} = \'{val}\'')

    # --------------------
    ## set a list of value in BuildInfo object
    #
    # @param name   the name of the list variable
    # @param items  the values of the list variable
    # @return None
    def _setlist(self, name, items):
        self._writeln(f'    {name} = [')
        for item in items:
            self._writeln(f'        \'{item}\',')
        self._writeln('    ]')

    # --------------------
    ## write a line to the build_info file
    # ensures it is terminated with a linefeed
    #
    # @param line  the line to write
    # @return None
    def _writeln(self, line):
        self._fp.write(f'{line}\n')

    # --------------------
    ## gen the current git SHA for the latest commit
    #
    # @return None
    def _gen_git_sha(self):
        tag = 'git SHA'
        rc, out = svc.utils_ps.run_cmd('git rev-parse --verify HEAD')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        self._set(tag, 'git_sha', out)

    # --------------------
    ## gen the current branch name
    #
    # @return None
    def _gen_git_branch(self):
        tag = 'git branch'

        rc, out = svc.utils_ps.run_cmd('git rev-parse --abbrev-ref HEAD')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        self._set(tag, 'git_branch', out)

    # --------------------
    ## show any uncommitted changes
    #
    # @return None
    def _gen_uncommitted_changes(self):
        tag = 'git uncommitted changes'
        rc, out = svc.utils_ps.run_cmd('git status -s')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        uncommitted = []
        count = self._get_failed_lines(tag, out, uncommitted, 'has uncommitted changes')
        self._exitrc += count

        self._setlist('git_uncommitted', uncommitted)

    # --------------------
    ## show any unpushed commits
    #
    # @return None
    def _gen_unpushed_commits(self):
        tag = 'git unpushed commits'
        rc, out = svc.utils_ps.run_cmd('git cherry -v')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        unpushed = []
        count = self._get_failed_lines(tag, out, unpushed, 'has unpushed changes')
        self._exitrc += count

        self._setlist('git_unpushed', unpushed)

    # --------------------
    ## gather and report failed lines in the given result lines
    #
    # @param tag           the logging tag
    # @param out           the output lines
    # @param failed_lines  the list to append any failed lines
    # @param suffix        the logging suffix if a warning occurs
    # @return the number of failed lines
    def _get_failed_lines(self, tag, out, failed_lines, suffix):
        header = False
        count = 0
        for line in out.split('\n'):
            if line != '':
                count += 1
                if not header:
                    if svc.gbl.verbose:
                        svc.log.warn(f'{tag: <25}:')
                    header = True
                failed_lines.append(line)
                if svc.gbl.verbose:
                    svc.log.warn(f'    {line}')

        if svc.gbl.verbose:
            if count == 0:
                svc.log.ok(f'{tag: <25}: none')
            else:
                svc.log.warn(f'{tag: <25}: {suffix}')
        return count
