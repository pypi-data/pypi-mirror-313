import unittest

import pytest
from medver_pytest import pth

from pyalamake.lib.list_param import ListParam
from ver.helpers import svc
from ver.helpers.helper import Helper


# pylint: disable=E1101
# pylint: disable=R0903

# -------------------
class TestTp090ListParam(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        cls.captured = None
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
    def test_tp090_list_param(self):
        pth.proto.protocol('tp-090', 'check list_param')
        pth.proto.add_objective('check the handling of parameters for compile/link')
        pth.proto.add_precondition('do_install has been run')

        self._check_simple_path()
        self._check_filter()
        self._check_accum_fn()
        self._check_remove()
        self._check_bad_types()
        self._check_bad_parm_type()

    # --------------------
    def _check_simple_path(self):
        pth.proto.step('check parm_type=path no filter, no accum')

        class App:
            def __init__(self):
                self._src_files = ListParam('sources', 'path',
                                            self, None, None)

        app = App()
        # initially empty
        pth.ver.verify_equal([], app.sources)
        # handle string
        app.add_sources('src1')
        pth.ver.verify_equal(['src1'], app.sources)
        # handle list of strings
        app.add_sources(['src2'])
        pth.ver.verify_equal(['src1', 'src2'], app.sources)
        # handle empty string or None
        app.add_sources('')
        pth.ver.verify_equal(['src1', 'src2'], app.sources)
        app.add_sources([''])
        pth.ver.verify_equal(['src1', 'src2'], app.sources)
        # ignore duplicate
        app.add_sources('src1')
        pth.ver.verify_equal(['src1', 'src2'], app.sources)
        app.add_sources(['src2'])
        pth.ver.verify_equal(['src1', 'src2'], app.sources)

    # --------------------
    def _check_filter(self):
        pth.proto.step('check parm_type=path with filter, no accum')

        class App:
            def __init__(self):
                self._src_files = ListParam('includes', 'path',
                                            self, self._skip_if, None)

            def _skip_if(self, val):
                return val.endswith('.cpp')

        app = App()
        app.add_includes('src1.h')
        app.add_includes('src2.cpp')  # should be skipped
        pth.ver.verify_equal(['src1.h'], app.includes)

    # --------------------
    def _check_accum_fn(self):
        pth.proto.step('check parm_type=string no filter, with accum')

        class App:
            def __init__(self):
                self.options = []
                self.add_options = lambda x: x
                self._opts_param = ListParam('options', 'string',
                                             self, None, self._accum_fn)
                self.opts = ''

            def _accum_fn(self):
                self.opts = ''
                for opt in self._opts_param.values:
                    self.opts += f'--{opt} '

        app = App()
        app.add_options('opt1')  # should match ListParams.tag
        app.add_options('opt2')
        pth.ver.verify_equal(['opt1', 'opt2'], app.options)
        pth.ver.verify_equal('--opt1 --opt2 ', app.opts)  # internal string has dashes

    # --------------------
    def _check_remove(self):
        pth.proto.step('check remove()')

        class App:
            def __init__(self):
                self.options = []
                self.add_options = lambda x: x
                self.remove_options = lambda x: x
                self._opts_param = ListParam('options', 'string',
                                             self, None, None)

                self.options2 = []
                self.add_options2 = lambda x: x
                self.remove_options2 = lambda x: x
                self._opts2_param = ListParam('options2', 'string',
                                              self, None, self._accum_fn)
                self.opts2 = []

            def _accum_fn(self):
                self.opts2 = ''
                for opt in self._opts_param.values:
                    self.opts2 += f'--{opt} '

        app = App()
        app.add_options('opt1')  # should match ListParams.tag
        app.add_options(['opt2', 'opt3', 'opt4'])
        pth.ver.verify_equal(['opt1', 'opt2', 'opt3', 'opt4'], app.options)
        app.remove_options('opt2')
        pth.ver.verify_equal(['opt1', 'opt3', 'opt4'], app.options)
        app.remove_options(['opt3', 'opt4'])
        pth.ver.verify_equal(['opt1'], app.options)

        app.add_options2('opt1')  # should match ListParams.tag
        app.add_options2(['opt2', 'opt3', 'opt4'])
        app.remove_options2(['opt3', 'opt4'])
        pth.ver.verify_equal(['opt1'], app.options)

        app.remove_options2('bad_opt')  # no warning or error
        pth.ver.verify_equal(['opt1'], app.options)

    # --------------------
    def _check_bad_types(self):
        pth.proto.step('check bad value type passed')

        class App:
            def __init__(self):
                self.add_stuff = lambda x: x
                self.remove_stuff = lambda x: x
                self._opts_param = ListParam('stuff', 'string',
                                             self, None, None)

        self.captured.readouterr()
        app = App()
        with pytest.raises(SystemExit) as excp:
            app.add_stuff(1.234)  # should raise excp
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        out, _ = self.captured.readouterr()
        pth.ver.verify_equal('ABRT stuff: can only add strings: 1.234 is <class \'float\'>', out.strip())

        with pytest.raises(SystemExit) as excp:
            app.add_stuff([2.345, 567])  # should raise excp
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        out, _ = self.captured.readouterr()
        pth.ver.verify_equal('ABRT stuff: accepts only str or list of str, 2.345 is <class \'float\'>', out.strip())

        with pytest.raises(SystemExit) as excp:
            app.remove_stuff(99)  # should raise excp
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        out, _ = self.captured.readouterr()
        pth.ver.verify_equal('ABRT stuff: can only remove strings: 99 is <class \'int\'>', out.strip())

        with pytest.raises(SystemExit) as excp:
            app.remove_stuff([32, 2.345])  # should raise excp
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        out, _ = self.captured.readouterr()
        pth.ver.verify_equal('ABRT stuff: accepts only str or list of str, 32 is <class \'int\'>', out.strip())

        # --------------------

    def _check_bad_parm_type(self):
        pth.proto.step('check bad value type passed')

        class App:
            def __init__(self):
                self._opts_param = ListParam('stuff', 'junk',
                                             self, None, None)

        self.captured.readouterr()
        with pytest.raises(SystemExit) as excp:
            app = App()  # pylint: disable=W0612 # noqa: F841
        pth.ver.verify_equal(SystemExit, excp.type)  # sys.exit abort
        out, _ = self.captured.readouterr()
        pth.ver.verify_equal('ABRT ListParm stuff: unknown type "junk"', out.strip())

    # --------------------
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.captured = capfd
