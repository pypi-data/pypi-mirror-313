from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a C++ target
class TargetCpp(TargetBase):
    # --------------------
    ## create a C++ target instance
    #
    # @param targets      current list of targets
    # @param target_name  name of new target to add
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetCpp(target_name)
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

    # --------------------
    ## return target type
    #
    # @return cpp target
    @property
    def target_type(self):
        return 'cpp'

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
            self._compile_opts_param.remove('-std=c++20')

    # --------------------
    ## check target for any issues
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

    # --------------------
    ## gen C++ target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_run()

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
    ## gen initial content for C++ target
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
    ## gen app build target
    #
    # @return None
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        build_deps = ''
        for file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = svc.osal.fix_path(dst_dir.replace(f'{svc.gbl.build_dir}/', ''))
            self.add_clean(f'{clean_path}/*.o')
            self.add_clean(f'{clean_path}/*.d')

            fixed_obj = svc.osal.fix_path(obj)
            fixed_file = svc.osal.fix_path(file)
            self._writeln(f'-include {svc.osal.fix_path(mmd_inc)}')
            self._writeln(f'{fixed_obj}: {fixed_file}')
            self._writeln(f'\t{self._cxx} -MMD -c {self._inc_dirs} {self._compile_opts} '
                          f'{fixed_file} -o {fixed_obj}')
            self._objs += f'{fixed_obj} '
            build_deps += f'{fixed_file} '

        self._writeln('')

        self._gen_rule(rule, self._objs, f'{self.target}: build source files')
        self._writeln('')

    # --------------------
    ## gen link target
    #
    # @return None
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        exe = f'{svc.gbl.build_dir}/{self.target}'
        fixed_exe = svc.osal.fix_path(exe)
        self._writeln(f'{fixed_exe}: {self._objs}')
        # FYI "-Xlinker -Map=debug/x.map" to see the contents
        self._writeln(f'\t{self._cxx} {self._objs} {self._link_opts} {self._link_paths} {self._libs} '
                      f'-o {fixed_exe}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(self.target)

        self._gen_rule(rule, exe, f'{self.target}: link')
        self._writeln('')

    # --------------------
    ## gen target to run c++ target
    #
    # @return None
    def _gen_run(self):
        rule = f'{self.target}-run'
        # don't add rule

        exe = f'{svc.gbl.build_dir}/{self.target}'

        self._gen_rule(rule, f'{self.target}-link', f'{self.target}: run executable, use s="args_here" to pass in args')
        self._writeln(f'\t@{svc.osal.fix_path(exe)} $(if $s, $s, )')
        self._writeln('')
