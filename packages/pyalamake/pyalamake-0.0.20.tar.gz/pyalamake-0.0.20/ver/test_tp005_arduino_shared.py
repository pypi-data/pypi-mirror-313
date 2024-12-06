import os.path
import unittest

import pytest
from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# pylint: disable=protected-access, too-many-statements

# -------------------
class TestTp005ArduinoShared(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        svc.helper = Helper()
        svc.helper.init()

    # -------------------
    def setUp(self):
        svc.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        svc.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        svc.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp005_arduino_shared(self):
        pth.proto.protocol('tp-005', 'gen for arduino shared components')
        pth.proto.add_objective('check the generation of an Arduino Shared component')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create arduino shared component, check initial values')
        sh1 = svc.mut.create_arduino_shared()
        self._check_initial(sh1)

        pth.proto.step('set boardid, check changes')
        self._check_boardid(sh1)

        sh1.set_avrdude_port('/dev/ttyUT')
        pth.ver.verify_equal('/dev/ttyUT', sh1.avrdude_port)

        pth.proto.step('create core')
        svc.mut.create('utcore', 'arduino-core', shared=sh1)
        svc.mut.ut_svc.log.ut_mode = True
        svc.mut.ut_svc.log.ut_lines = []
        failed = False
        try:
            sh1.check()
        except SystemExit:
            failed = True
        pth.ver.verify_false(failed, reqids=['srs-154'])  # check() should not abort
        pth.ver.verify_equal(0, len(svc.mut.ut_svc.log.ut_lines))

        pth.proto.step('print board list')
        svc.mut.ut_svc.log.ut_mode = True
        svc.mut.ut_svc.log.ut_lines = []
        sh4 = svc.mut.create_arduino_shared()
        sh4.print_board_list()
        # TODO works if -k tp005, fails otherwise
        # # length depends on content of boards.json
        # pth.ver.verify_equal(39, len(svc.mut.ut_svc.log.ut_lines))
        # pth.ver.verify_equal('     Available boards:', svc.mut.ut_svc.log.ut_lines[0])
        # pth.ver.verify_equal('        yun                 : Arduino Yún', svc.mut.ut_svc.log.ut_lines[1])
        # pth.ver.verify_equal('        uno                 : Arduino Uno', svc.mut.ut_svc.log.ut_lines[2])

        pth.proto.step('ensure check() fails when missing core')
        sh2 = svc.mut.create_arduino_shared()
        sh2.set_boardid('uno')
        sh2.set_avrdude_port('/dev/ttyUT2')

        svc.mut.ut_svc.log.ut_mode = True
        svc.mut.ut_svc.log.ut_lines = []
        with pytest.raises(SystemExit) as excp:
            sh2.check()  # should abort
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        pth.ver.verify_equal(4, len(svc.mut.ut_svc.log.ut_lines))
        pth.ver.verify_equal('ERR  arduino: core_tgt is not set', svc.mut.ut_svc.log.ut_lines[0])
        pth.ver.verify_equal('ERR  arduino: coredir is not set', svc.mut.ut_svc.log.ut_lines[1])
        pth.ver.verify_equal('ERR  arduino: corelib is not set', svc.mut.ut_svc.log.ut_lines[2])
        pth.ver.verify_equal('ERR  arduino: corelib_name is not set', svc.mut.ut_svc.log.ut_lines[3])

        pth.proto.step('ensure invalid boardid() fails')
        svc.mut.ut_svc.log.ut_mode = True
        svc.mut.ut_svc.log.ut_lines = []
        sh3 = svc.mut.create_arduino_shared()
        with pytest.raises(SystemExit) as excp:
            sh3.set_boardid('xxuno')  # should abort
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-155'])  # sys.exit abort
        pth.ver.verify_equal(0, len(svc.mut.ut_svc.log.ut_lines))  # the abort line is done with a print()

    # --------------------
    def _check_initial(self, sh1):
        pth.ver.verify_none(sh1.boardid, reqids=['srs-150', 'srs-151'])
        pth.ver.verify_none(sh1.avrdude_port)

        # these are from /usr/share/arduino/hardware/arduino/avr/boards.txt
        # see boards.json
        pth.ver.verify_none(sh1.f_cpu)
        pth.ver.verify_none(sh1.mcu)
        pth.ver.verify_none(sh1.avrdude)
        pth.ver.verify_none(sh1.avrdude_baudrate)
        pth.ver.verify_none(sh1.avrdude_protocol)

        # these are derived from the above
        pth.ver.verify_none(sh1.common_opts)
        pth.ver.verify_none(sh1.cpp_opts)
        pth.ver.verify_none(sh1.cc_opts)

        # === tools

        # these are only for ubuntu based arduino
        home = os.path.expanduser('~')
        if svc.mut.is_macos:
            pth.ver.verify_equal(f'{home}/Library/Arduino15', sh1.arduino_dir, reqids=['srs-152'])
            pth.ver.verify_equal('/opt/homebrew/etc', sh1.avrdude_dir)
        elif svc.mut.is_win:
            pth.ver.verify_equal('C:\\Users\\micro/AppData/Local/Arduino15', sh1.arduino_dir, reqids=['srs-152'])
            pth.ver.verify_equal(
                'C:\\Users\\micro/AppData/Local/Arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/etc',
                sh1.avrdude_dir)
        else:
            pth.ver.verify_equal('/usr/share/arduino', sh1.arduino_dir, reqids=['srs-152'])
            pth.ver.verify_equal('/usr/share/arduino/hardware/tools', sh1.avrdude_dir)

        pth.ver.verify_equal('avr-g++', sh1.cpp)
        pth.ver.verify_equal('avr-gcc', sh1.cc)
        pth.ver.verify_equal('avr-ar', sh1.ar)
        pth.ver.verify_equal('avr-objcopy', sh1.obj_copy)

        # === core related
        pth.ver.verify_none(sh1.core_tgt)  # name of core target
        pth.ver.verify_none(sh1.corelib)  # path to core lib
        pth.ver.verify_none(sh1.corelib_name)  # name of the lib
        pth.ver.verify_none(sh1.coredir)  # the build dir

        # these are only for ubuntu based arduino
        if svc.mut.is_macos:
            path = f'{sh1.arduino_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino'
        elif svc.mut.is_win:
            path = f'{sh1.arduino_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino'
        else:
            path = f'{sh1.arduino_dir}/hardware/arduino/avr/cores/arduino'
        pth.ver.verify_equal(path, sh1.core_includes[0], reqids=['srs-152'])
        if svc.mut.is_macos:
            path = f'{sh1.arduino_dir}/packages/arduino/hardware/avr/1.8.6/variants/standard'
        elif svc.mut.is_win:
            path = f'{sh1.arduino_dir}/packages/arduino/hardware/avr/1.8.6/variants/standard'
        else:
            path = f'{sh1.arduino_dir}/hardware/arduino/avr/variants/standard'
        pth.ver.verify_equal(path, sh1.core_includes[1])

    # --------------------
    def _check_boardid(self, sh1):
        sh1.set_boardid('mega-atmega2560')
        pth.ver.verify_equal('mega-atmega2560', sh1.boardid, reqids=['srs-153'])
        # these values are from boards.json (assumed correct)
        pth.ver.verify_equal('16000000', sh1.f_cpu, reqids=['srs-153'])
        pth.ver.verify_equal('atmega2560', sh1.mcu)
        pth.ver.verify_equal('avrdude', sh1.avrdude)
        pth.ver.verify_equal('115200', sh1.avrdude_baudrate)
        pth.ver.verify_equal('wiring', sh1.avrdude_protocol)

        # these are derived from the above
        pth.ver.verify_equal('-MMD -c -ffunction-sections -fdata-sections -mmcu=atmega2560 '
                             '-DF_CPU=16000000L -DUSB_VID=null -DUSB_PID=null -DARDUINO=106',
                             sh1.common_opts)
        pth.ver.verify_equal('-MMD -c -ffunction-sections -fdata-sections -mmcu=atmega2560 '
                             '-DF_CPU=16000000L -DUSB_VID=null -DUSB_PID=null -DARDUINO=106 '
                             '-fno-exceptions -fno-threadsafe-statics -std=c++11',
                             sh1.cpp_opts)
        pth.ver.verify_equal('-MMD -c -ffunction-sections -fdata-sections -mmcu=atmega2560 '
                             '-DF_CPU=16000000L -DUSB_VID=null -DUSB_PID=null -DARDUINO=106',
                             sh1.cc_opts)
