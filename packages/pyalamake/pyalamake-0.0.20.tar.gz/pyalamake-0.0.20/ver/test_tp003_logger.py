import unittest

from medver_pytest import pth

from pyalamake.lib.logger import Logger as pyalog
from ver.helpers import svc
from ver.helpers.helper import Helper


# pylint: disable=too-many-statements

# -------------------
class TestTp003Logger(unittest.TestCase):
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
    def test_tp003_logger(self):
        pth.proto.protocol('tp-003', 'logger behavior')
        pth.proto.add_objective('check Logger functions as expected')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pyalog.ut_mode = True

        # === check
        pth.proto.step('check() behaviors')
        pyalog.ut_lines = []
        pyalog.check(True, 'check true')
        pyalog.check(False, 'check false')
        pth.ver.verify_equal(2, len(pyalog.ut_lines), reqids=['srs-120'])
        pth.ver.verify_equal('OK   check true', pyalog.ut_lines[0])
        pth.ver.verify_equal('ERR  check false', pyalog.ut_lines[1])

        # === check
        pth.proto.step('check_all() behaviors')
        pyalog.ut_lines = []
        pyalog.check_all(True, 'check_all', ['true1', 'true2'])
        pyalog.check_all(False, 'check_all', ['false1', 'false2'])
        pth.ver.verify_equal(6, len(pyalog.ut_lines), reqids=['srs-120'])
        pth.ver.verify_equal('OK   check_all: True', pyalog.ut_lines[0])
        pth.ver.verify_equal('OK      - true1', pyalog.ut_lines[1])
        pth.ver.verify_equal('OK      - true2', pyalog.ut_lines[2])
        pth.ver.verify_equal('ERR  check_all: False', pyalog.ut_lines[3])
        pth.ver.verify_equal('ERR     - false1', pyalog.ut_lines[4])
        pth.ver.verify_equal('ERR     - false2', pyalog.ut_lines[5])

        # === output()
        pth.proto.step('check output() behaviors')
        pyalog.ut_lines = []
        pyalog.output('out1')  # no lineno
        pyalog.output('out2')
        pyalog.output('out3', 3)  # with lineno
        pyalog.output('out4', 4)
        pth.ver.verify_equal(4, len(pyalog.ut_lines), reqids=['srs-120'])
        pth.ver.verify_equal(' --     out1', pyalog.ut_lines[0])
        pth.ver.verify_equal(' --     out2', pyalog.ut_lines[1])
        pth.ver.verify_equal(' --  3] out3', pyalog.ut_lines[2])
        pth.ver.verify_equal(' --  4] out4', pyalog.ut_lines[3])

        # === one liners
        pth.proto.step('simple logging behaviors')
        pyalog.ut_lines = []
        pyalog.start('start')
        pyalog.line('line')
        pyalog.highlight('highlight')
        pyalog.ok('ok')
        pyalog.err('err')
        pyalog.bug('bug')
        pyalog.warn('warn')
        pyalog.dbg('dbg')
        pyalog.raw('raw')
        pth.ver.verify_equal(9, len(pyalog.ut_lines), reqids=['srs-120'])
        pth.ver.verify_equal('==== start', pyalog.ut_lines[0])
        pth.ver.verify_equal('     line', pyalog.ut_lines[1])
        pth.ver.verify_equal('---> highlight', pyalog.ut_lines[2])
        pth.ver.verify_equal('OK   ok', pyalog.ut_lines[3])
        pth.ver.verify_equal('ERR  err', pyalog.ut_lines[4])
        pth.ver.verify_equal('BUG  bug', pyalog.ut_lines[5])
        pth.ver.verify_equal('WARN warn', pyalog.ut_lines[6])
        pth.ver.verify_equal('DBG  dbg', pyalog.ut_lines[7])
        pth.ver.verify_equal('raw', pyalog.ut_lines[8])

        # === verbose off
        pth.proto.step('simple logging behaviors')
        pyalog.ut_lines = []
        pyalog.verbose = False
        pyalog.check(True, 'check false')
        pyalog.check(False, 'check false')  # print always
        pyalog.check_all(True, 'check_all', ['true1', 'true2'])
        pyalog.check_all(False, 'check_all', ['false1', 'false2'])  # print always
        pyalog.start('start')
        pyalog.line('line')
        pyalog.highlight('highlight')
        pyalog.ok('ok')
        pyalog.err('err')  # print always
        pyalog.bug('bug')  # print always
        pyalog.warn('warn')
        pyalog.dbg('dbg')
        pyalog.raw('raw')
        pth.ver.verify_equal(6, len(pyalog.ut_lines), reqids=['srs-121'])
        pth.ver.verify_equal('ERR  check false', pyalog.ut_lines[0])
        pth.ver.verify_equal('ERR  check_all: False', pyalog.ut_lines[1])
        pth.ver.verify_equal('ERR     - false1', pyalog.ut_lines[2])
        pth.ver.verify_equal('ERR     - false2', pyalog.ut_lines[3])
        pth.ver.verify_equal('ERR  err', pyalog.ut_lines[4])
        pth.ver.verify_equal('BUG  bug', pyalog.ut_lines[5])
