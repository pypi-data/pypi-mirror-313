import unittest

import pytest
from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp008Pyalamake(unittest.TestCase):
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
    def test_tp008_pyalamake(self):
        pth.proto.protocol('tp-008', 'remaining pyalamake functions')
        pth.proto.add_objective('check the remaining functions in pyalamake main')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('check gbl()')
        pth.ver.verify_equal('debug', svc.mut.gbl.build_dir)
        svc.mut.gbl.set_build_dir('release')
        pth.ver.verify_equal('release', svc.mut.gbl.build_dir, reqids=['srs-180'])

        pth.proto.step('check invalid target type')
        with pytest.raises(SystemExit) as excp:
            svc.mut.create('bad', 'unknown')
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-181'])  # sys.exit abort
