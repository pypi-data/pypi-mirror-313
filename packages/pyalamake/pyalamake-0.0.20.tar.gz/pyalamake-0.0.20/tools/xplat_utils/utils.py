import os
import sys

# these must NOT require external imports otherwise will fail when venv doesn't exist
from .cfg import Cfg
from .do_clean import DoClean
from .gen_files import GenFiles
from .svc import svc
from .utils_common import UtilsCommon
from .utils_fs import UtilsFs
from .utils_logger import UtilsLogger
from .utils_ps import UtilsPs


# --------------------
## holds mainline for all utilities
class Utils(UtilsCommon):
    # --------------------
    ## gen bash set_cfg.sh file for use in bash scripts
    #
    # @return None
    def gen_bash_cfg(self):
        self._init('gen_bash_cfg')

        path = os.path.join('tools', 'set_cfg.sh')
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write('#! /usr/bin/env bash\n')

            val = self.get_cfg('mod_name')
            fp.write(f'export cmn_mod_name="{val}"\n')

            val = self.get_cfg('mod_dir_name')
            fp.write(f'export cmn_mod_dir_name="{val}"\n')

            val = str(svc.utils_fs.convert_relative_to_abs(svc.gbl.outdir))
            fp.write(f'export OUT_DIR="{val}"\n')

            val = self.get_cov_opts()
            fp.write(f'export COV_OPTS="{val}"\n')

    # --------------------
    ## create the output directory
    #
    # @return None
    def create_outdir(self):
        self._init('create_out_dir')
        svc.utils_fs.create_outdir()
        # Note: no _term()

    # --------------------
    ## recreate subdirectory in output directory
    #
    # @param subdir the subdirectory to create
    # @return None
    def recreate_outsubdir(self, subdir):
        self._init('recreate_outsubdir')
        svc.utils_fs.clean_out_dir(subdir)
        # Note: no _term()

    # --------------------
    ## check if any python pip modules are out of date
    #
    # @return None
    def pip_outofdate(self):
        self._init('pip_outofdate')
        svc.log.line('out of date modules in tools/requirements.txt')
        # Note: old 'pip3 install --upgrade -r tools/requirements.txt --dry-run --quiet'
        cmd = 'pip3 list --outdated'
        svc.utils_ps.run_process(cmd)
        svc.log.check(svc.gbl.rc == 0, f'out of date rc={svc.gbl.rc}')
        # Note: no _term()

    # --------------------
    ## initialize cfg values and generate version.json
    #
    # @param dogen   generate files
    # @param subdir  (optional) subdir to place files into
    # @return None
    def gen_files(self, dogen='', subdir=''):
        self._set_params(False)
        self._init('gen_files')
        svc.gen_files.all(dogen=dogen, subdir=subdir)
        # Note: no _term()

    # TODO delete after GenConstants and GenBuildInfo merged into GenFiles
    # # --------------------
    # ## initialize generate constants files
    # #
    # # @param subdir  (optional) subdir to place files into
    # # @return None
    # def gen_constants(self, subdir=None):
    #     from .gen_constants import GenConstants
    #     self._set_params(False)
    #     self._init('gen_constants')
    #     impl = GenConstants()
    #     impl.run(subdir)
    #     self._term(False)
    #
    # # --------------------
    # ## initialize generate constants files
    # #
    # # @param subdir  (optional) subdir to place files into
    # # @return None
    # def gen_build_info(self, subdir=None):
    #     from .gen_build_info import GenBuildInfo
    #     self._set_params(False)
    #     self._init('gen_build_info')
    #     impl = GenBuildInfo()
    #     impl.run(subdir)
    #     self._term(False)

    # --------------------
    ## mainline for the do_clean operation.
    # removes all generated files and subdirectories.
    # The root directory should be equivalent to a clean git clone
    #
    # @param subdir  directory where gen_files are placed
    # @param depth   cleaning action depth: full, lite
    # @return None
    def do_clean(self, subdir='', depth=''):
        self._init('do_clean')
        impl = DoClean()
        impl.run(subdir=subdir, depth=depth)
        self._term(True)

    # --------------------
    ## mainline for the do_check operation.
    # checks all versions
    #
    # @return None
    def do_check(self):
        verbose = True
        from .do_check import DoCheck
        self._set_params(verbose)
        self._init('do_check')
        impl = DoCheck()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_doc operation.
    # runs doxygen on all files specified in Doxyfile
    #
    # @param make_pdf  generate the PDF (default) or not (False)
    # @return None
    def do_doc(self, make_pdf=True):
        from .do_doc import DoDoc
        self._set_params(True)
        self._init('do_doc')
        impl = DoDoc()
        impl.run(make_pdf)
        self._term(True)

    # --------------------
    ## mainline for the do_lint operation.
    # runs pylint on all given source files
    #
    # @param dogen  generate files or not
    # @param subdir (optional) subdir to place files into
    # @param tool  for cpp/arduino use clang-tidy or cppcheck
    # @return None
    def do_lint(self, dogen='', subdir='', tool=''):
        from .do_lint import DoLint
        verbose = False
        self._set_params(verbose)
        self._init('do_lint')
        svc.gen_files.all(dogen=dogen, subdir=subdir)
        impl = DoLint()
        impl.run(tool)
        self._term(verbose)

    # --------------------
    # DEPRECATED but still used by swig-c and swig-cpp
    ## mainline for the do_build operation.
    # runs cmake on source files
    #
    # @param verbose     True for additional verbosity
    # @param build_type  build type: debug or release
    # @param tech        technology: cpp or arduino
    # @param target      the cmake target to build e.g. ut
    # @return None
    def do_build(self, verbose, build_type='debug', tech=None, target=None):
        from .do_build import DoBuild
        self._set_params(verbose)
        self._init('do_build')
        impl = DoBuild()
        impl.run(tech, build_type, target)
        self._term(verbose)

    # --------------------
    ## mainline for the do_ver_info operation.
    # generate version info files
    #
    # @return None
    def do_ver_info(self):
        verbose = True
        from .do_ver_info import DoVerInfo
        self._set_params(verbose)
        self._init('do_ver_info')
        impl = DoVerInfo()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_publish operation.
    # post the verification data
    #
    # @return None
    def do_post_ver(self):
        verbose = True
        from .do_post_ver import DoPostVer
        self._set_params(verbose)
        self._init('do_post_ver')
        impl = DoPostVer()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_publish operation.
    # generate the setup.py file
    #
    # @param dogen  generate files or not
    # @param subdir (optional) subdir to place files into
    # @return None
    def do_publish(self, dogen='', subdir=''):
        verbose = False
        from .do_publish import DoPublish
        self._set_params(verbose)
        self._init('do_publish')
        svc.gen_files.all(dogen=dogen, subdir=subdir)
        impl = DoPublish()
        impl.run()
        # script also reports overallrc; set verbose False to prevent
        self._term(False)

    # === do_xx: UT related

    # note python does not have a do_ut() see below for C++/Arduino

    # --------------------
    ## mainline for the do_coverage operation.
    #
    # @param action      reset or gen
    # @return None
    def do_coverage(self, action=None):
        verbose = True
        from .do_coverage import DoCoverage
        self._set_params(verbose)
        self._init('do_coverage')
        impl = DoCoverage()
        impl.run(action)
        self._term(False)

    # === C++/Arduino related

    # --------------------
    ## mainline for the do_makefile operation.
    #
    # @param target      the makefile target to build e.g. all
    # @return None
    def do_makefile(self, target='all'):
        verbose = False
        from .do_makefile import DoMakefile
        self._set_params(verbose)
        self._init('do_makefile')
        impl = DoMakefile()
        impl.run(target)
        self._term(verbose)

    # === C++/Arduino UT related

    # --------------------
    ## mainline for the do_makefile_coverage operations.
    #
    # @param action      reset or gen
    # @param target      the target to generate coverage for
    # @return None
    def do_makefile_coverage(self, action, target):
        verbose = False
        from .do_makefile_coverage import DoMakefileCoverage
        self._set_params(verbose)
        self._init('do_makefile_coverage')
        impl = DoMakefileCoverage()
        impl.run(action, target)
        self._term(False)

    # === CPIP related

    # --------------------
    ## mainline for the do_cpip operation.
    #
    # @param action      publish or pull
    # @return None
    def do_cpip(self, action):
        verbose = True
        from .do_cpip import DoCpip
        self._set_params(verbose)
        self._init('do_cpip')
        impl = DoCpip()
        impl.run(action)
        self._term(verbose)

    # --------------------
    ## get cpip pkg info
    #
    # @param pkg_name   the package to get info about
    # @return None
    def cpip_get(self, pkg_name):
        from .do_cpip import DoCpip
        self._set_params(False)
        self._init('do_cpip')
        impl = DoCpip()
        return impl.get(pkg_name)

    # === common utility functions

    # TODO move to utils_common or to utils_fs
    # --------------------
    ## takes the given path and converts it a path relative to home, e.g,
    # * ~/out    => ~/out
    # * ./out    => ~/projects/proj1/out
    # * out      => ~/projects/proj1/out
    #
    # @param path the path to convert
    # @return the converted path
    def convert_relative_to_home(self, path):
        path1 = os.path.expanduser(path)
        path2 = os.path.abspath(path1)
        homedir = os.path.expanduser('~')
        path3 = path2.replace(homedir, '~')
        return path3

    # === support functions related

    # --------------------
    ## set the class parameters used to run mainline functions
    #
    # @param verbose       whether the function should run with verbose logging or not
    # @return None
    def _set_params(self, verbose):
        svc.gbl.verbose = verbose

    # --------------------
    ## initialization.
    # sets logging tag and overallrc to 0
    #
    # @param tag  the logging tag to use
    # @return None
    def _init(self, tag):
        svc.gbl.tag = tag
        svc.gbl.rc = 0
        svc.gbl.overallrc = 0

        # must be before Cfg, etc.
        svc.log = UtilsLogger

        svc.cfg = Cfg
        svc.utils_fs = UtilsFs()
        svc.utils_ps = UtilsPs()
        svc.gen_files = GenFiles()

        # load cfg if necessary
        svc.cfg.load(svc.utils_fs.root_dir)
        # uncomment for debug
        # svc.cfg.report()

    # --------------------
    ## terminate.
    # reports overall rc
    #
    # @param verbose  flag for log verbosity
    # @return None
    def _term(self, verbose=True):
        # hack; some functions are not setting overallrc correctly
        if svc.gbl.overallrc == 0 and svc.gbl.rc != 0:
            svc.gbl.overallrc = svc.gbl.rc

        if verbose:
            svc.log.check(svc.gbl.overallrc == 0, f'{svc.gbl.tag}: overall rc={svc.gbl.overallrc}')
        sys.exit(svc.gbl.overallrc)
