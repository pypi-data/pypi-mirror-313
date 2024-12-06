import unittest

import pytest
from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# pylint: disable=protected-access, too-many-statements

# -------------------
class TestTp002TargetBase(unittest.TestCase):
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
    def test_tp002_target_base(self):
        pth.proto.protocol('tp-002', 'common behavior in target base')
        pth.proto.add_objective('check TargetBase functions for setting common args')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create target that uses TargetBase')
        tgt = svc.mut.create('cpp2', 'cpp')
        # check property target()
        pth.ver.verify_equal('cpp2', tgt.target)
        pth.ver.verify_equal([], tgt.sources, reqids=['srs-100'])  # initially empty
        pth.ver.verify_equal([], tgt.include_directories, reqids=['srs-100'])  # initially empty

        # --- rules
        pth.ver.verify_equal([], tgt.rules, reqids=['srs-100'])
        tgt.add_rule('ut_rule')
        pth.ver.verify_equal(['ut_rule'], tgt.rules, reqids=['srs-101'])

        # --- clean
        pth.ver.verify_equal({}, tgt.clean, reqids=['srs-100'])
        tgt.add_clean('*.c')
        pth.ver.verify_equal({'*.c': 1}, tgt.clean)
        tgt.add_clean('*.c')
        pth.ver.verify_equal({'*.c': 1}, tgt.clean)  # does not duplicate
        # gen all clean targets so far
        tgt.gen_clean()
        pth.ver.verify_equal(4, len(tgt.lines))
        pth.ver.verify_equal('#-- cpp2: clean files in this target', tgt.lines[0])
        pth.ver.verify_equal('cpp2-clean:', tgt.lines[1])
        pth.ver.verify_equal('\trm -f debug/*.c', tgt.lines[2], reqids=['srs-102'])
        pth.ver.verify_equal('', tgt.lines[3])

        # --- sources
        tgt.add_sources('src1')  # add a string
        pth.ver.verify_equal(['src1'], tgt.sources, reqids=['srs-002'])  # has added source
        tgt.add_sources(['src2', 'src3'])  # add a list
        pth.ver.verify_equal(['src1', 'src2', 'src3'], tgt.sources, reqids=['srs-002'])  # has added source
        with pytest.raises(SystemExit) as excp:
            tgt.add_sources(1)  # should abort
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-103'])  # sys.exit abort

        # --- duplicate target
        with pytest.raises(SystemExit) as excp:
            svc.mut.create('cpp2', 'cpp')
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-105'])  # sys.exit abort

        # --- include dirs
        tgt = svc.mut.create('cpp2a', 'cpp')  # use a unique target name
        tgt.add_include_directories('inc1')  # add a string
        pth.ver.verify_equal(['inc1'], tgt.include_directories, reqids=['srs-003'])  # has added include dirs
        tgt.add_include_directories(['inc2', 'inc3'])  # add a list
        pth.ver.verify_equal(['inc1', 'inc2', 'inc3'], tgt.include_directories,
                             reqids=['srs-003'])  # has added include dirs
        pth.ver.verify_equal('"-Iinc1" "-Iinc2" "-Iinc3" ', tgt._inc_dirs,
                             reqids=['srs-003'])  # check internal has prefixes
        with pytest.raises(SystemExit) as excp:
            tgt.add_include_directories(1)  # should abort
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-104'])  # sys.exit abort
        tgt = svc.mut.create('cpp2b', 'cpp')  # use a unique target name
        with pytest.raises(SystemExit) as excp:
            tgt.add_include_directories(['inc4', 1])  # add a list with a bad value
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-104'])  # sys.exit abort

        # --- link libraries
        tgt = svc.mut.create('cpp2c', 'cpp')  # use a unique target name
        tgt.add_link_libraries('lib1')  # add a string
        pth.ver.verify_equal(['lib1'], tgt.link_libraries, reqids=['srs-005'])  # has added include dirs
        tgt.add_link_libraries(['lib2', 'lib3'])  # add a list
        pth.ver.verify_equal(['lib1', 'lib2', 'lib3'], tgt.link_libraries, reqids=['srs-005'])  # has added include dirs
        pth.ver.verify_equal('-llib1 -llib2 -llib3 ', tgt._libs, reqids=['srs-005'])  # check internal has prefixes
        with pytest.raises(SystemExit) as excp:
            tgt.add_link_libraries(1)  # should abort
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-106'])  # sys.exit abort
        tgt = svc.mut.create('cpp2d', 'cpp')  # use a unique target name
        with pytest.raises(SystemExit) as excp:
            tgt.add_link_libraries([1, 'lib4'])  # add a list with a bad value
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-106'])  # sys.exit abort

        # --- link files
        tgt = svc.mut.create('cpp2e', 'cpp')  # use a unique target name
        tgt.add_link_files('file1')  # add a string
        pth.ver.verify_equal(['file1'], tgt.link_files, reqids=['srs-006'])  # has added include dirs
        tgt.add_link_files(['file2', 'file3'])  # add a list
        pth.ver.verify_equal(['file1', 'file2', 'file3'], tgt.link_files, reqids=['srs-006'])  # has added include dirs
        pth.ver.verify_equal('"file1" "file2" "file3" ', tgt._libs, reqids=['srs-006'])  # check internal has prefixes

        # ensure mix of libraries and files are ok
        tgt.add_link_libraries('lib1')  # add a string
        pth.ver.verify_equal(['lib1'], tgt.link_libraries, reqids=['srs-005'])  # has added include dirs
        pth.ver.verify_equal(['file1', 'file2', 'file3'], tgt.link_files, reqids=['srs-006'])  # has added include dirs
        pth.ver.verify_equal('-llib1 "file1" "file2" "file3" ', tgt._libs,
                             reqids=['srs-005', 'srs-006'])  # check internal has prefixes

        with pytest.raises(SystemExit) as excp:
            tgt.add_link_files(1)  # should abort
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-107'])  # sys.exit abort
        tgt = svc.mut.create('cpp2f', 'cpp')  # use a unique target name
        with pytest.raises(SystemExit) as excp:
            tgt.add_link_files([1, 'lib4'])  # add a list with a bad value
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-107'])  # sys.exit abort
