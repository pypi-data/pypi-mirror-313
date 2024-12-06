from .svc import svc
from .target_base import TargetBase


# --------------------
## target for an Arduino app
class TargetArduino(TargetBase):
    # --------------------
    ## create an Arduino target
    #
    # @param targets      current list of targets
    # @param target_name  name of the new target
    # @param shared       info for shared core
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduino(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  name of the new target
    # @param shared       info for shared core
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        if shared is None:
            svc.abort('Arduino Targets must have a shared Arduino Core component passed in')

        ## shared Arduino Core info
        self._shared = shared

        ## compile options
        self.add_compile_options(self._shared.debug_compile_opts)  # pylint: disable=E1101

        ## build directories
        self._build_dirs = {}

        # these need to be set below
        ## target build directory
        self.tgt_build_dir = None
        ## ELF file generated for this app
        self._elffile = None
        ## EEP file generated for this app
        self._eepfile = None
        ## HEX file generated for this app
        self._hexfile = None
        ## list of target dependencies for this app
        self._app_deps = None

    # --------------------
    ## type of this target
    # @return arduino target
    @property
    def target_type(self):
        return 'arduino'

    # --------------------
    ## update include directories params string
    #
    # @return None
    def _update_inc_dirs(self):
        super()._update_inc_dirs()
        for incdir in self._shared.core_includes:
            self._inc_dirs += f' "-I{svc.osal.fix_path(incdir)}" '

    # --------------------
    ## add an arduino library to list of libraries.
    # these libraries are recognized:
    #  * Servo
    #
    # @param lib  the library to add
    # @return None
    def add_library(self, lib):
        if lib == 'Servo':
            svc.log.line(f'adding arduino library: {lib}')
            self.add_sources(f'{self._shared.library_root}/Servo/src/avr/Servo.cpp')  # pylint: disable=E1101
            self.add_include_directories(f'{self._shared.library_root}/Servo/src')  # pylint: disable=E1101
            self.add_compile_options('-DARDUINO_ARCH_AVR')  # pylint: disable=E1101
        else:
            svc.abort(f'{self.target} target_arduino: unknown arduino library: {lib}')

    # --------------------
    ## check various aspects of parameters
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino: resolve errors')

    # --------------------
    ## generate Arduino target
    #
    # @return None
    def gen_target(self):
        self.tgt_build_dir = f'{svc.gbl.build_dir}/{self.target}-dir'

        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')
        svc.log.line(f'   boardid  : {self._shared.boardid}')
        svc.log.line(f'   port     : {self._shared.avrdude_port}')
        svc.log.line(f'   baud_rate: {self._shared.avrdude_baudrate}')
        svc.log.line(f'   mcu      : {self._shared.mcu}')
        svc.log.line(f'   tgt dir  : {self.tgt_build_dir}')
        svc.log.line(f'   corelib  : {self._shared.corelib}')
        svc.log.line(f'   coredir  : {self._shared.coredir}')

        self._elffile = f'{svc.gbl.build_dir}/{self.target}.elf'
        self.add_clean(f'{self.target}.elf')

        self._eepfile = f'{svc.gbl.build_dir}/{self.target}.eep'
        self.add_clean(f'{self.target}.eep')

        self._hexfile = f'{svc.gbl.build_dir}/{self.target}.hex'
        self.add_clean(f'{self.target}.hex')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_upload()

    # --------------------
    ## generate arguments for build
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:  # pylint: disable=E1101
            _, _, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    ## generate initialization rule
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
    ## generate build rule
    #
    # @return None
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        # assumes _app_deps is only used in writeln()
        self._app_deps = ''
        build_deps = ''
        for file in self.sources:  # pylint: disable=E1101
            obj, mmd_inc, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = dst_dir.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{svc.osal.fix_path(clean_path)}/*.o')
            self.add_clean(f'{svc.osal.fix_path(clean_path)}/*.d')

            self._writeln(f'-include {svc.osal.fix_path(mmd_inc)}')
            self._writeln(f'{svc.osal.fix_path(obj)}: {svc.osal.fix_path(file)}')
            self._writeln(f'\t{self._shared.cpp} {self._shared.cpp_opts} '
                          f'{self._compile_opts} {self._inc_dirs} '
                          f'{svc.osal.fix_path(file)} -o {svc.osal.fix_path(obj)}')
            self._app_deps += f'{svc.osal.fix_path(obj)} '
            build_deps += f'{svc.osal.fix_path(file)} '

        self._writeln('')

        self._gen_rule(rule, build_deps, f'{self.target}: build sketch')
        self._writeln('')

    # --------------------
    ## generate link rule
    #
    # @return None
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        self._gen_rule(rule, f'{self._shared.core_tgt} {self._hexfile}',
                       f'{self.target}: link sketch and core')
        self._writeln('')

        # creates the ELF
        self._writeln(f'{svc.osal.fix_path(self._elffile)}: {self._app_deps} {svc.osal.fix_path(self._shared.corelib)}')
        self._writeln(f'\t{self._shared.cc} -Os -Wl,--gc-sections -mmcu={self._shared.mcu} '
                      f'-o {svc.osal.fix_path(self._elffile)} '
                      f'{self._app_deps} '
                      f'{svc.osal.fix_path(self._shared.corelib)} -lm')
        self._writeln('')

        # creates the EEP
        self._writeln(f'{svc.osal.fix_path(self._eepfile)}: {svc.osal.fix_path(self._elffile)}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load '
                      f'--no-change-warnings --change-section-lma .eeprom=0 '
                      f'{svc.osal.fix_path(self._elffile)} {svc.osal.fix_path(self._eepfile)}')
        self._writeln('')

        # creates the HEX
        self._writeln(f'{svc.osal.fix_path(self._hexfile)}: '
                      f'{svc.osal.fix_path(self._elffile)} {svc.osal.fix_path(self._eepfile)}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -R .eeprom '
                      f'{svc.osal.fix_path(self._elffile)} {svc.osal.fix_path(self._hexfile)}')
        self._writeln('')

    # --------------------
    ## generate upload rule
    #
    # @return None
    def _gen_upload(self):
        rule = f'{self.target}-upload'
        # don't add rule

        avrdude_conf = f'{self._shared.avrdude_dir}/avrdude.conf'
        avrdude_protocol = self._shared.avrdude_protocol
        avrdude_args = f'-C{svc.osal.fix_path(avrdude_conf)} -p{self._shared.mcu} -c{avrdude_protocol} ' \
                       f'-P{self._shared.avrdude_port} -b{self._shared.avrdude_baudrate}'

        self._gen_rule(rule, f'{self.target}-link', f'{self.target}: upload to arduino')
        self._writeln(f'\t{self._shared.avrdude} -v {avrdude_args} -D '
                      f'-Uflash:w:{svc.osal.fix_path(self._hexfile)}:i '
                      f'-Ueeprom:w:{svc.osal.fix_path(self._eepfile)}:i')
        self._writeln('')
