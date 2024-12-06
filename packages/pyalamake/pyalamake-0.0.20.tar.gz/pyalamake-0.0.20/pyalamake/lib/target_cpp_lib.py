from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a C++ Library target, static (default) or shared
# see https://renenyffenegger.ch/notes/development/languages/C-C-plus-plus/GCC/create-libraries/index
class TargetCppLib(TargetBase):
    # --------------------
    ## create a C++ libary instance
    #
    # @param targets      current list of targets
    # @param target_name  name of new target to add
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetCppLib(target_name)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  the name of this target
    def __init__(self, target_name):
        super().__init__(target_name)

        ## list of object files
        self._objs = ''
        ## compiler to use
        self._cxx = 'c++'
        ## list of compile options
        self.add_compile_options(['-std=c++20', '-D_GNU_SOURCE'])  # pylint: disable=E1101

        ## list of build directories
        self._build_dirs = {}

        ## library type: static, shared
        self._lib_type = 'static'

    # --------------------
    ## return target type
    #
    # @return cpp target
    @property
    def target_type(self):
        return 'cpp-lib'

    # --------------------
    ## return compiler to use
    # @return compiler to use
    @property
    def compiler(self):
        return self._cxx

    # --------------------
    ## set compiler to use
    # @param val  the compiler setting
    # @return None
    @compiler.setter
    def compiler(self, val):
        self._cxx = val
        if self._cxx == 'gcc':
            self._compile_opts_parm.remove('-std=c++20')  # pylint: disable=E1101

    # --------------------
    ## set the library type to generate
    #
    # @param val  the type to set: static or shared
    def set_type(self, val):
        valid_types = ['static', 'shared']
        if val not in valid_types:
            svc.abort(f'invalid library type, expected {valid_types}, actual: {val}')
        self._lib_type = val

    # --------------------
    ## check target for any issues
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

    # --------------------
    ## gen C++ library target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_lib()
        if self._lib_type == 'shared':
            self._gen_shared_library()
        else:
            self._gen_static_library()

    # --------------------
    ## create output directory
    #
    # @return None
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:  # pylint: disable=E1101
            _, _, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    ## gen initial content for C++ library
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
    ## gen lib build target
    #
    # @return None
    def _gen_lib(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        build_deps = ''
        for file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = dst_dir.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{svc.osal.fix_path(clean_path)}/*.o')
            self.add_clean(f'{svc.osal.fix_path(clean_path)}/*.d')

            self._writeln(f'-include {svc.osal.fix_path(mmd_inc)}')
            self._writeln(f'{svc.osal.fix_path(obj)}: {svc.osal.fix_path(file)}')
            fpic = ''
            if self._lib_type == 'shared':
                fpic = '-fPIC '
            self._writeln(f'\t{self._cxx} -MMD {fpic} -c {self._inc_dirs} {self._compile_opts} '
                          f'{svc.osal.fix_path(file)} -o {svc.osal.fix_path(obj)}')
            self._objs += f'{svc.osal.fix_path(obj)} '
            build_deps += f'{svc.osal.fix_path(file)} '

        self._writeln('')

        self._gen_rule(rule, self._objs, f'{self.target}: build source files')
        self._writeln('')

    # --------------------
    ## gen shared library
    #
    # @return None
    def _gen_shared_library(self):
        rule = f'{self.target}-shared'
        self.add_rule(rule)

        if svc.gbl.os_name == 'win':
            extension = 'dll'
        else:
            extension = 'so'
        lib_name = f'lib{self.target}.{extension}'
        lib = f'{svc.gbl.build_dir}/{lib_name}'
        self._writeln(f'{svc.osal.fix_path(lib)}: {self._objs}')
        self._writeln(
            f'\t{self._cxx} -MMD --shared -fPIC {self._objs} {self._link_opts} {self._link_paths} {self._libs} '
            f'-o {svc.osal.fix_path(lib)}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(lib_name)

        self._gen_rule(rule, lib, f'{self.target}: link')
        self._writeln('')

    # --------------------
    ## gen static library
    #
    # @return None
    def _gen_static_library(self):
        rule = f'{self.target}-shared'
        self.add_rule(rule)

        lib_name = f'lib{self.target}.a'
        lib = f'{svc.gbl.build_dir}/{lib_name}'
        self._writeln(f'{svc.osal.fix_path(lib)}: {self._objs}')
        self._writeln(
            f'\tar rcs {svc.osal.fix_path(lib)} {self._objs} {self._link_opts} {self._link_paths} {self._libs}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(lib_name)

        self._gen_rule(rule, lib, f'{self.target}: link')
        self._writeln('')
