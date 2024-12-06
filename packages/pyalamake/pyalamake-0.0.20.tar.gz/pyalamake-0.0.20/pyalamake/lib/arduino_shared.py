import json
import os

from .svc import svc


# --------------------
## Shared info for Arduino Core targets and arduino targets
class ArduinoShared:
    ## board id of the arduino; set by user
    boardid = None
    ## avrdude port to use
    avrdude_port = None

    # these are from /usr/share/arduino/hardware/arduino/avr/boards.txt
    ## the CPU id
    f_cpu = None
    ## the MCU id
    mcu = None
    ## the avrdude to use
    avrdude = None
    ## the avrdude baud rate to use for this board
    avrdude_baudrate = None
    ## the avrdude protocol to use for this board
    avrdude_protocol = None
    # these are derived from the above
    ## common compile options
    common_opts = None
    ## C++ compile options
    cpp_opts = None
    ## C compile options
    cc_opts = None

    ## debug compile options
    debug_compile_opts = None

    ## arduino directory that holds common files and arduino library
    arduino_dir = None
    ## arduino AVR C++ compiler
    cpp = None
    ## arduino AVR C compiler
    cc = None
    ## arduino AVR linker
    ar = None
    ## arduino copies an object file
    obj_copy = None
    ## path to avrdude
    avrdude_dir = None

    # core related
    ## name of core target
    core_tgt = None
    ## path to core lib
    corelib = None
    ## name of the core lib
    corelib_name = None
    ## the path to the core lib
    coredir = None
    ## additional include directories for the arduino library
    core_includes = []

    ## holds library root directory
    library_root = ''

    # --------------------
    ## constructor
    def __init__(self):
        ## debug compile options
        self.debug_compile_opts = ['-g', '-Os', '-Wall']

        ## arduino directory that holds common files and arduino library
        self.arduino_dir = svc.osal.arduino_root_dir()
        ## arduino AVR C++ compiler
        self.cpp = 'avr-g++'
        ## arduino AVR C compiler
        self.cc = 'avr-gcc'
        ## arduino AVR linker
        self.ar = 'avr-ar'
        ## arduino copies an object file
        self.obj_copy = 'avr-objcopy'
        ## path to avrdude.conf
        self.avrdude_dir = svc.osal.avrdude_dir(self.arduino_dir)

        ## additional include directories for the arduino library
        self.core_includes = svc.osal.arduino_core_includes(self.arduino_dir)

    # --------------------
    ## set location of the root directory
    #
    # @param rootdir  the path to the root dir
    # @return None
    def set_library_root(self, rootdir):
        ## see ArduinoShared.Library_root
        self.library_root = rootdir

    # --------------------
    ## set the avrdude port
    #
    # @param val   the port to use
    # @return None
    def set_avrdude_port(self, val):
        self.avrdude_port = val
        self._check_port_exists(val)

    # --------------------
    ## print the list of known Arduino boards
    #
    # @return None
    def print_board_list(self):
        boards = self._get_board_json()
        svc.log.line('Available boards:')
        for name, info in boards.items():
            svc.log.line(f'   {name: <20}: {info["fullname"]}')

    # --------------------
    ## check common arduino values
    #
    # @return None
    def check(self):
        errs = 0
        errs = self._check_arg(errs, 'boardid')
        errs = self._check_arg(errs, 'avrdude_port')
        errs = self._check_arg(errs, 'f_cpu')
        errs = self._check_arg(errs, 'mcu')
        errs = self._check_arg(errs, 'avrdude')
        errs = self._check_arg(errs, 'avrdude_baudrate')
        errs = self._check_arg(errs, 'avrdude_protocol')
        errs = self._check_arg(errs, 'common_opts')
        errs = self._check_arg(errs, 'cpp_opts')
        errs = self._check_arg(errs, 'cc_opts')

        errs = self._check_arg(errs, 'core_tgt')
        errs = self._check_arg(errs, 'coredir')
        errs = self._check_arg(errs, 'corelib')
        errs = self._check_arg(errs, 'corelib_name')

        if errs > 0:
            svc.abort('arduino: resolve errors')

    # --------------------
    ## check argument for arduino board
    #
    # @param errs   current number of errs
    # @param arg    the argument to check
    # @return the updated errs value
    def _check_arg(self, errs, arg):
        selfarg = getattr(self, arg, None)
        if selfarg is None:
            errs += 1
            svc.log.err(f'arduino: {arg} is not set')
        return errs

    # --------------------
    ## set board id for this shared component
    #
    # @param boardid the board id
    # @return None
    def set_boardid(self, boardid):
        info = self._get_board_info(boardid)
        self.boardid = boardid

        # set values based on board id
        self.f_cpu = info['build.f_cpu']
        self.mcu = info['build.mcu']
        self.avrdude = info['upload.tool']
        self.avrdude_baudrate = info['upload.speed']
        self.avrdude_protocol = info['upload.protocol']

        self.common_opts = f'-MMD -c -ffunction-sections -fdata-sections ' \
                           f'-mmcu={self.mcu} -DF_CPU={self.f_cpu}L ' \
                           '-DUSB_VID=null -DUSB_PID=null -DARDUINO=106'
        self.cpp_opts = f'{self.common_opts} -fno-exceptions -fno-threadsafe-statics -std=c++11'
        self.cc_opts = self.common_opts

    # --------------------
    ## get board info based on the boardid
    #
    # @param boardid  the board id to search for
    # @return info found
    def _get_board_info(self, boardid):
        boards = self._get_board_json()
        if boardid not in boards:
            svc.abort(f'arduino: invalid boardid: {boardid}')

        info = boards[boardid]
        return info

    # --------------------
    ## load board info from the boards.json file
    #
    # @return the board info
    def _get_board_json(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'boards.json')
        with open(path, 'r', encoding='utf-8') as fp:
            boards = json.load(fp)
            return boards

    # --------------------
    ## check if a serial port exists
    #
    # @param port   the port to check
    # @return None
    def _check_port_exists(self, port):
        try:
            import serial
        except ModuleNotFoundError:
            svc.log.warn(f'{"arduino_shared": <15}: module pyserial is not installed')
            return

        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        foundit = False
        for found_port, desc, hwid in sorted(ports):
            if port == found_port:
                foundit = True
                svc.log.line(f'{"arduino_shared": <15}: found port {port}: {desc} [{hwid}]')
                break
        if not foundit:
            svc.log.warn(f'{"arduino_shared": <15}: port {port} not found')
