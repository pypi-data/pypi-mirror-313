import os

from .list_param import ListParam
from .svc import svc


# --------------------
## base class for all targets
class TargetBase:  # pylint: disable=too-many-instance-attributes
    # --------------------
    ## constructor
    #
    # @param target_name  the target name
    def __init__(self, target_name):
        ## target name
        self._target = target_name

        # note;  the lambda functions help Pycharm and pylint to resolve to dynamically allocated functions

        # === compile related

        ## list of sources property
        self.sources = []
        ## stub for add_sources function
        self.add_sources = lambda x: x
        ## list of source files parameter
        self._src_files_param = ListParam('sources', 'path',
                                          ## see function _sources_skip_if()
                                          self, self._sources_skip_if, None)

        ## list of include property
        self.include_directories = []
        ## stub for add_include_directories function
        self.add_include_directories = lambda x: x
        ## param string for include directories
        self._inc_dirs = ''
        ## list of include directories parameter
        self._inc_dirs_param = ListParam('include_directories', 'path',
                                         ## see function _update_inc_dirs
                                         self, None, self._update_inc_dirs)

        ## stub for compile_options property
        self.compile_options = []
        ## stub for add_compile_options function
        self.add_compile_options = lambda x: x
        ## param string for compilation options
        self._compile_opts = ''
        ## list of compile options parameter
        self._compile_opts_param = ListParam('compile_options', 'string',
                                             ## see function _update_compile_opts
                                             self, None, self._update_compile_opts)

        # === link related

        ## stub for link_options property
        self.link_options = []
        ## stub for add_link_options function
        self.add_link_options = lambda x: x
        ## list of link options
        self._link_opts = ''
        ## list of link options parameter
        self._link_opts_param = ListParam('link_options', 'string',
                                          ## see function _update_link_opts
                                          self, None, self._update_link_opts)

        ## stub for add_link_libraries property
        self.link_libraries = []
        ## stub for add_link_libraries function
        self.add_link_libraries = lambda x: x
        ## stub for link_files property
        self.link_files = []
        ## stub for add_link_files function
        self.add_link_files = lambda x: x
        ## param string for link libraries and files
        self._libs = ''
        ## list link libraries for this target; holds shortened library names i.e. no "lib" prefix, no ".a" extension
        self._link_libs_param = ListParam('link_libraries', 'string',
                                          ## see function _update_link_libs
                                          self, None, self._update_link_libs)
        ## list of paths to link files for this target; holds full path and library name
        self._link_files_param = ListParam('link_files', 'path',
                                           ## see function _update_link_libs
                                           self, None, self._update_link_libs)

        ## stub for add_link_directories property
        self.link_directories = []
        ## stub for add_link_directories function
        self.add_link_directories = lambda x: x
        ## param string for link paths
        self._link_paths = ''
        ## list link directories this target;  holds paths to search for libraries
        self._link_paths_param = ListParam('link_directories', 'path',
                                           ## see function _update_link_libs
                                           self, None, self._update_link_paths)

        ## info for the clean rule for this target
        self._clean = {}
        ## info for cleaning the coverage generated
        self._clean_cov = {}

        ## help for this target
        self._help = {}
        ## list of rules for this target
        self._rules = []
        ## list of lines in the makefile for all aspects of this target
        self._lines = []

    # --------------------
    ## return the name of this target
    # @return the name of this target
    @property
    def target(self):
        return self._target

    # === target rules

    # --------------------
    ## add a new rule for this target
    #
    # @param rule  the name of the rule
    def add_rule(self, rule):
        self._rules.append(rule)

    # --------------------
    ## return the list of rules for this target
    # @return list of rules
    @property
    def rules(self):
        return self._rules

    # === clean rules

    # --------------------
    ## add clean target to list of patterns to clean
    #
    # @param pattern   the pattern to add
    # @return None
    def add_clean(self, pattern):
        if pattern not in self._clean:
            self._clean[pattern] = 1

    # --------------------
    ## return list of clean patterns for this target
    # @return return list of clean patterns
    @property
    def clean(self):
        return self._clean

    # === help text

    # --------------------
    ## add halp line for the given rule
    #
    # @param rule   the rule this help applies to
    # @param desc   the description for this help
    # @return None
    def _add_help(self, rule, desc):
        if rule in self._help:
            svc.log.warn(f'add_help: target "{rule}" already has description')
            svc.log.warn(f'   prev: {self._help[rule]}')
            svc.log.warn(f'   curr: {desc}')
            svc.log.warn('   replacing...')
        self._help[rule] = desc

    # --------------------
    ## return current help lines
    # @return list of help lines
    @property
    def help(self):
        return self._help

    # === source files

    # --------------------
    ## skip if a passed in source file value is an include file
    #
    # @param val   the source file to check
    # @return True if it is an include file (ends with .h) or False otherwise
    def _sources_skip_if(self, val):
        return val.endswith('.h')

    # === include directories

    # --------------------
    ## update include directories parameter to use in command line
    #
    # @return None
    def _update_inc_dirs(self):
        self._inc_dirs = ''
        for inc_dir in self._inc_dirs_param.values:
            self._inc_dirs += f'"-I{svc.osal.fix_path(inc_dir)}" '

    # === compilation/link flags

    # --------------------
    ## update the compile options parameter based on the current list of options
    #
    # @return None
    def _update_compile_opts(self):
        self._compile_opts = ''
        for opt in self._compile_opts_param.values:
            self._compile_opts += f'{opt} '

    # --------------------
    ## update the link options parameter based on the current list of options
    #
    # @return None
    def _update_link_opts(self):
        self._link_opts = ''
        for opt in self._link_opts_param.values:
            self._link_opts += f'{opt} '

    # === link libraries

    # --------------------
    ## update the link libraries command line info
    #
    # @return None
    def _update_link_libs(self):
        ## see base class for self._libs
        self._libs = ''

        ## see base class for self._link_libs
        for lib in self._link_libs_param.values:
            self._libs += f'-l{lib} '

        ## see base class for self._link_files
        for file in self._link_files_param.values:
            self._libs += f'"{file}" '

    # --------------------
    ## update the link directory paths command line info
    #
    # @return None
    def _update_link_paths(self):
        self._link_paths = ''
        for link_dir in self._link_paths_param.values:
            self._link_paths += f'-L{link_dir} '

    # === macos specific

    # --------------------
    ## update homebrew library and include directories for macOS.
    # ignored if not macOS.
    #
    # @return None
    def add_homebrew(self):
        if svc.gbl.os_name == 'macos':
            self.add_link_directories(svc.osal.homebrew_link_dirs())  # pylint: disable=E1101
            self.add_include_directories(svc.osal.homebrew_inc_dirs())  # pylint: disable=E1101

    # === gen functions

    # --------------------
    ## generate a path to an object file in this target
    #
    # @param file  the filename to use for the object file
    # @return obj: path to object file, dst_dir: path to the directory the object file is in
    def _get_obj_path(self, file):
        obj = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.o'
        obj = obj.replace('//', '/')

        mmd_inc = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.d'
        mmd_inc = mmd_inc.replace('//', '/')

        dst_dir = os.path.dirname(obj)
        return obj, mmd_inc, dst_dir

    # --------------------
    ## generate a rule
    #
    # @param rule   the rule's name
    # @param deps   the dependencies on this rule
    # @param desc   the description for this rule (comment in the makefile)
    def _gen_rule(self, rule, deps, desc):
        self._writeln(f'#-- {desc}')
        self._add_help(rule, desc)
        if deps:
            self._writeln(f'{rule}: {deps}')
        else:
            self._writeln(f'{rule}:')

    # --------------------
    ## generate line to reset coverage info
    #
    # @param reset_rule  the name of the reset rule
    # @return None
    def _gen_reset_coverage(self, reset_rule):
        self._gen_rule(reset_rule, '', f'{self.target}: reset coverage info')

        for pattern in self._clean_cov:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    ## generate lines to clean and generated directories and files given
    #
    # @return None
    def gen_clean(self):
        clean_cov_rule = ''
        if self._clean_cov:
            reset_rule = f'{self.target}-cov-reset'
            self._gen_reset_coverage(reset_rule)
            clean_cov_rule = reset_rule

        rule = f'{self.target}-clean'
        self._gen_rule(rule, clean_cov_rule, f'{self.target}: clean files in this target')

        patterns = {}
        for pattern in self.clean:
            patterns[pattern] = 1
        for pattern in patterns:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    ## various common checks for valid info
    #
    # @return None
    def _common_check(self):
        for file in self._src_files_param.values:
            if not os.path.isfile(file):
                svc.log.warn(f'{self.target}: source file {file} not found')

        for inc_dir in self._inc_dirs_param.values:
            if not os.path.isdir(inc_dir):
                svc.log.warn(f'{self.target}: include directory {inc_dir} not found')

        # _link_libs_param  # can't do, these may be generated
        # _link_files_param # can't do, these may be generated

    # === for writing to Makefile

    # --------------------
    ## return the list of lines for this target
    #
    # @return the list of lines
    @property
    def lines(self):
        return self._lines

    # --------------------
    ## save the given line to be generated later
    #
    # @param line  the line to write
    # @return None
    def _writeln(self, line):
        self._lines.append(line)
