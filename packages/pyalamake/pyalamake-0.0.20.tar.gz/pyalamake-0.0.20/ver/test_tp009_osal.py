import unittest

from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp009Osal(unittest.TestCase):
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
    def test_tp009_osal_ubu(self):
        pth.proto.protocol('tp-009', 'check osal conversions')
        pth.proto.add_objective('check the OSAL functions for cross-platform behavior')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('check OSAL fix_path() for ubuntu')
        svc.mut.gbl.os_name = 'ubuntu'
        pth.ver.verify_equal('/usr/bin/file1', svc.mut.osal.fix_path('/usr/bin/file1'))
        pth.ver.verify_equal('/usr/bin/file2', svc.mut.osal.fix_path('/usr\\bin//file2'))

        pth.proto.step('check OSAL fix_path() for macos')
        svc.mut.gbl.os_name = 'macos'
        pth.ver.verify_equal('/usr/bin/file1', svc.mut.osal.fix_path('/usr/bin/file1'))
        pth.ver.verify_equal('/usr/bin/file2', svc.mut.osal.fix_path('/usr\\bin//file2'))

        pth.proto.step('check OSAL fix_path() for win')
        svc.mut.gbl.os_name = 'win'
        pth.ver.verify_equal('/c/User/bob/file1', svc.mut.osal.fix_path('C:\\User\\bob\\file1'))
        pth.ver.verify_equal('/d/User/bob/file2', svc.mut.osal.fix_path('D:\\User\\bob\\file2'))
        pth.ver.verify_equal('/y/User/bob/file3', svc.mut.osal.fix_path('Y:\\User\\bob/file3'))
        pth.ver.verify_equal('/c/User/bob/file4', svc.mut.osal.fix_path('/c/User/bob/file4'))

        # with prefixes
        pth.ver.verify_equal('pre/fix/c/User/bob/file1', svc.mut.osal.fix_path('pre/fix/C:\\User\\bob\\file1'))
        pth.ver.verify_equal('pre/fix/d/User/bob/file2', svc.mut.osal.fix_path('pre/fix/D:\\User\\bob\\file2'))
        pth.ver.verify_equal('pre/fix/y/User/bob/file3', svc.mut.osal.fix_path('pre/fix/Y:\\User\\bob/file3'))
        pth.ver.verify_equal('pre/fix/c/User/bob/file4', svc.mut.osal.fix_path('pre/fix//c/User/bob/file4'))
