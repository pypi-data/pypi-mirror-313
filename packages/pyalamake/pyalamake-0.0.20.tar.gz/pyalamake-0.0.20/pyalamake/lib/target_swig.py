import os
import pathlib

from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a SWIG target
class TargetSwig(TargetBase):
    # --------------------
    ## create a SWIG target instance
    #
    # @param targets      current list of targets
    # @param target_name  name of new target to add
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetSwig(target_name)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  the name of this target
    def __init__(self, target_name):
        super().__init__(target_name)

        ## the swig target engine
        self._engine = None
        ## list of generated files
        self._genned = []
        ## list of additional swig options
        self._swig_opts = ''
        ## indicate if -c++ option
        self._cpp = False
        ## list of build directories
        self._build_dirs = {}

    # --------------------
    ## return target type
    #
    # @return cpp target
    @property
    def target_type(self):
        return 'swig'

    # --------------------
    ## set compiler to use
    # @return None
    def set_cpp(self):
        self._cpp = True

    # --------------------
    ## generate the given code for the swig target engine
    #
    # @param arg  the engine type
    # @return None
    def engine(self, arg):
        if arg == 'ruby':
            self._engine = '-ruby'
        elif arg == 'python':
            self._engine = '-python'
        elif arg == 'jsc':
            self._engine = '-javascript -jsc'
        elif arg == 'v8':
            self._engine = '-javascript -v8'
        elif arg == 'node':
            self._engine = '-javascript -node'
        elif arg == 'napi':
            self._engine = '-javascript -napi'

    # --------------------
    ## additional options for swig command
    #
    # @param opts  additional options
    # @return None
    def opts(self, opts):
        self._swig_opts = opts

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
        self._gen_files()

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
            self._writeln(f'\t@mkdir -p {blddir}')
        self._writeln('')

    # --------------------
    ## gen source files based on swig
    #
    # @return None
    def _gen_files(self):
        rule = f'{self.target}-gen'
        self.add_rule(rule)

        if self._cpp:
            extension = 'cpp'
            self._swig_opts += '-c++ '
        else:
            extension = 'c'

        # should be list of ".i" files
        self._genned = []
        genned_files = ''
        for file in self.sources:  # pylint: disable=E1101
            gen_file = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.{extension}'
            gen_file = gen_file.replace('//', '/')
            dst_dir = os.path.dirname(gen_file)
            pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)

            # gen clean paths
            clean_path = gen_file.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{clean_path}/*.{extension}')

            self._writeln(f'{gen_file}: {file}')
            self._writeln(f'\tswig {self._engine} {self._swig_opts} -o {gen_file} {file} ')
            self._genned.append(gen_file)
            genned_files += f'{gen_file} '

        self._writeln('')

        self._gen_rule(rule, genned_files, f'{self.target}: genned source files')
        self._writeln('')
