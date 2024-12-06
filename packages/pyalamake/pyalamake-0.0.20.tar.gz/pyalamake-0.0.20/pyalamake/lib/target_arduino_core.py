import glob

from pyalamake.lib.svc import svc
from pyalamake.lib.target_base import TargetBase


# --------------------
## target for an Arduino Core
class TargetArduinoCore(TargetBase):
    # --------------------
    ## create an Arduino Core target
    #
    # @param targets      current list of targets
    # @param target_name  name of the new target
    # @param shared       the shared core info
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduinoCore(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  name of the new target
    # @param shared       the shared core info
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        ## shared info
        self._shared = shared
        ## shared core target
        self._shared.core_tgt = target_name
        ## shared core directory
        self._shared.coredir = f'{svc.gbl.build_dir}/{self._shared.core_tgt}-dir'
        ## shared core library name
        self._shared.corelib_name = f'{self._shared.core_tgt}.a'
        ## shared core library path
        self._shared.corelib = f'{svc.gbl.build_dir}/{self._shared.corelib_name}'

        ## compile options to use
        self.add_compile_options(self._shared.debug_compile_opts)  # pylint: disable=E1101

        ## build directories to use
        self._build_dirs = {}

        ## library directory to use
        self._libdir = None
        ## list of object files to use
        self._objs = []
        ## list of include directories
        self._inc_dirs = []

    # --------------------
    ## the arduino core type
    # @return target type
    @property
    def target_type(self):
        return 'arduino_core'

    # --------------------
    ## check for various conditions in this target
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino_core: resolve errors')

    # --------------------
    ## generate this target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'gen target {self.target}, type:{self.target_type}')

        self._gen_args()
        self._gen_init()

        self.add_clean(self._shared.corelib_name)

        self._libdir = svc.osal.arduino_core_libdir(self._shared.arduino_dir)

        self._inc_dirs = ''
        for incdir in self._shared.core_includes:
            self._inc_dirs += f' "-I{svc.osal.fix_path(incdir)}" '

        self._gen_core_compile()
        self._gen_core_link()
        self._writeln('')

    # --------------------
    ## generate argues for the build directory
    #
    # @return None
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1
        self._build_dirs[self._shared.coredir] = 1

        self._writeln('')

    # --------------------
    ## generate init rule
    #
    # @return None
    def _gen_init(self):
        rule = f'{self.target}-init'
        self.add_rule(rule)

        self._gen_rule(rule, '', f'{self.target}: initialize for {svc.gbl.build_dir} build')
        for blddir in self._build_dirs:
            self._writeln(f'\t@mkdir -p {svc.osal.fix_path(blddir)}')
        self._writeln('')

    # --------------------
    ## generate core compilation rule
    #
    # @return None
    def _gen_core_compile(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        cpp_files = self._gen_core_cpp_compile()
        c_files = self._gen_core_c_compile()

        # add clean rules; the clean function automatically adds the build_dir
        self.add_clean(f'{self._shared.core_tgt}-dir/*.o')
        self.add_clean(f'{self._shared.core_tgt}-dir/*.d')

        src_deps = ''
        for (src, _, _) in sorted(cpp_files + c_files):
            src_deps += f' {svc.osal.fix_path(src)}'

        self._gen_rule(rule, src_deps, f'{self.target}: compile arduino core source files')
        self._writeln('')

    # --------------------
    ## generate list of source files for C++ compilation
    #
    # @return list of source files
    def _gen_core_cpp_compile(self):
        src_files = []
        for src in glob.glob(f'{self._libdir}/*.cpp', recursive=True):
            obj = src.replace(self._libdir, self._shared.coredir) + '.o'
            mmd_inc = src.replace(self._libdir, self._shared.coredir) + '.d'
            src_files.append((src, mmd_inc, obj))

        for src, mmd_inc, obj in sorted(src_files):
            self._writeln(f'-include {svc.osal.fix_path(mmd_inc)}')
            self._writeln(f'{svc.osal.fix_path(obj)}: {svc.osal.fix_path(src)}')
            self._writeln(f'\t{self._shared.cpp} {self._shared.cpp_opts} '
                          f'{self._inc_dirs} {self._compile_opts} '
                          f'{svc.osal.fix_path(src)} -o {svc.osal.fix_path(obj)}')
            self._objs.append(obj)

        self._writeln('')

        return src_files

    # --------------------
    ## generate list of source files for C compilation
    #
    # @return list of source files
    def _gen_core_c_compile(self):
        src_files = []
        for src in glob.glob(f'{self._libdir}/*.c', recursive=True):
            obj = src.replace(self._libdir, self._shared.coredir) + '.o'
            mmd_inc = src.replace(self._libdir, self._shared.coredir) + '.d'
            src_files.append((src, mmd_inc, obj))

        for src, mmd_inc, obj in sorted(src_files):
            self._writeln(f'-include {svc.osal.fix_path(mmd_inc)}')
            self._writeln(f'{svc.osal.fix_path(obj)}: {svc.osal.fix_path(src)}')
            self._writeln(f'\t{self._shared.cc} {self._shared.cc_opts} '
                          f'{self._inc_dirs} {self._compile_opts} '
                          f'{svc.osal.fix_path(src)} -o {svc.osal.fix_path(obj)}')
            self._objs.append(obj)

        self._writeln('')

        return src_files

    # --------------------
    ## generate link rule
    #
    # @return None
    def _gen_core_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        self._gen_rule(rule, self._shared.corelib, f'{self.target}: create arduino core library')
        self._writeln('')

        obj_deps = ''
        for obj in self._objs:
            obj_deps += f' {svc.osal.fix_path(obj)}'
        self._writeln(f'{self._shared.corelib}: {obj_deps}')
        self._writeln(f'\trm -f {self._shared.corelib}')
        for obj in sorted(self._objs):
            self._writeln(f'\t{self._shared.ar} rcs {self._shared.corelib} {svc.osal.fix_path(obj)}')
