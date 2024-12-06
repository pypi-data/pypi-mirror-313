import unittest

import pytest
from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp007ArduinoTarget(unittest.TestCase):
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
    def test_tp007_arduino_target(self):
        pth.proto.protocol('tp-007', 'gen for arduino targets')
        pth.proto.add_objective('check the generation of an Arduino target')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create arduino_shared component')
        sh1 = svc.mut.create_arduino_shared()
        sh1.set_boardid('uno')
        sh1.set_avrdude_port('/dev/ttyACM0')

        core = svc.mut.create('core1', 'arduino-core', shared=sh1)
        core.check()

        pth.proto.step('create arduino target')
        tgt = svc.mut.create('ino1', 'arduino', shared=sh1)
        pth.ver.verify_equal('ino1', tgt.target)
        pth.ver.verify_equal('arduino', tgt.target_type, reqids=['srs-170'])  # arduino exists
        pth.ver.verify_equal([], tgt.sources)  # initially empty
        pth.ver.verify_equal([], tgt.include_directories)  # initially empty

        # --- sources
        tgt.add_sources('src1')  # add a string
        pth.ver.verify_equal(['src1'], tgt.sources, reqids=['srs-002'])  # has added source
        tgt.add_sources(['src2', 'src3'])  # add a list
        pth.ver.verify_equal(['src1', 'src2', 'src3'], tgt.sources, reqids=['srs-002'])  # has added source
        # TODO set_sources()

        # --- include dirs
        tgt.add_include_directories('inc1')  # add a string
        pth.ver.verify_equal(['inc1'], tgt.include_directories, reqids=['srs-003'])  # has added include dirs
        tgt.add_include_directories(['inc2', 'inc3'])  # add a list
        pth.ver.verify_equal(['inc1', 'inc2', 'inc3'], tgt.include_directories,
                             reqids=['srs-003'])  # has added include dirs
        # TODO set_include_directories()

        # --- link libraries and files
        tgt.add_link_libraries('lib1')  # add a string
        pth.ver.verify_equal(['lib1'], tgt.link_libraries, reqids=['srs-005'])  # has added library
        tgt.add_link_libraries(['lib2', 'lib3'])  # add a list
        pth.ver.verify_equal(['lib1', 'lib2', 'lib3'], tgt.link_libraries,
                             reqids=['srs-005'])  # has added link libraries
        tgt.add_link_files('mylib')  # add a string
        pth.ver.verify_equal(['mylib'], tgt.link_files, reqids=['srs-006'])  # has added link libraries

        # --- values set during gen_target()
        svc.mut.makefile(svc.helper.makefile_path)

        pth.ver.verify_equal(['ino1-init', 'ino1-build', 'ino1-link'], tgt.rules)
        # targets to clean
        pth.ver.verify_equal({
            'ino1-dir/*.o': 1,  # obj files
            'ino1-dir/*.d': 1,  # dependecy files
            'ino1.eep': 1,  # eep for main exec
            'ino1.elf': 1,  # elf for main exec
            'ino1.hex': 1,  # main executable
        }, tgt.clean)

        pth.proto.step('create arduino target without a shared component')
        with pytest.raises(SystemExit) as excp:
            svc.mut.create('ino2', 'arduino')
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-171'])  # sys.exit abort
