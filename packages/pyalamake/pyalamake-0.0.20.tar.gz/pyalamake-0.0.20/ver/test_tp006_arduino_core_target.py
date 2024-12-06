import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp006ArduinoCoreTarget(unittest.TestCase):
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
    def test_tp006_arduino_core_target(self):
        pth.proto.protocol('tp-006', 'gen for arduino core targets')
        pth.proto.add_objective('check the generation of an Arduino Core target')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create arduino_shared component')
        sh1 = svc.mut.create_arduino_shared()
        sh1.set_boardid('uno')
        sh1.set_avrdude_port('/dev/ttyACM0')

        pth.proto.step('create core')
        core = svc.mut.create('core', 'arduino-core', shared=sh1)
        pth.ver.verify_equal('core', core.target)
        pth.ver.verify_equal('arduino_core', core.target_type, reqids=['srs-160'])  # core exists

        failed = False
        try:
            core.check()
        except SystemExit:
            failed = True
        pth.ver.verify_false(failed, reqids=['srs-161'])  # check() should not abort

        # --- values set during gen_target()
        svc.mut.makefile(svc.helper.makefile_path)

        pth.ver.verify_equal(['core-init', 'core-build', 'core-link'], core.rules)
        # targets to clean
        pth.ver.verify_equal({
            'core.a': 1,  # core lib
            'core-dir/*.o': 1,  # obj files
            'core-dir/*.d': 1,  # obj files
        }, core.clean)
