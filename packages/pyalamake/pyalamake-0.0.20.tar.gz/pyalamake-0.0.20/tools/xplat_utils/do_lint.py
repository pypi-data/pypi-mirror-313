import glob
import os

from .svc import svc


# --------------------
## perform the do_lint operation
class DoLint:
    # --------------------
    ## do_lint mainline.
    #
    # @param tool   for python: pylint (default) or ruff; for cpp: cppcheck or clang-tidy(default)
    # @return None
    def run(self, tool):
        if svc.cfg.mod_tech == 'python' and not tool:
            tool = 'pylint'
        elif svc.cfg.mod_tech in ['cpp', 'arduino'] and not tool:
            tool = 'cppcheck'

        svc.log.highlight(f'{svc.gbl.tag}: starting tech:{svc.cfg.mod_tech} tool:{tool}...')
        if svc.cfg.mod_tech == 'python':
            self._run_python(tool)
        elif svc.cfg.mod_tech in ['cpp', 'arduino']:
            # arduino defaults to same as C++
            self._run_cpp(tool)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tech:{svc.cfg.mod_tech}, use one of: python, cpp, arduino')

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: pylint rc={svc.gbl.rc}')

    # --------------------
    ## run pylint
    #
    # @param tool  the tool to use; valid values depend on current tech
    # @return None
    def _run_python(self, tool):
        # always run pycodestyle
        svc.log.highlight(f'{svc.gbl.tag}: running pycodestyle')
        svc.utils_ps.run_process('pycodestyle', use_raw_log=True)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: pycodestyle rc={svc.gbl.rc}')

        if tool == 'pylint':
            svc.log.highlight(f'{svc.gbl.tag}: running pylint')
            dirs = self._get_dirs()
            rc_path = self._find_pylintrc()
            cmd = f'pylint --rcfile={rc_path} {dirs}'
            svc.utils_ps.run_process(cmd, use_raw_log=True)
        elif tool == 'ruff':
            svc.log.highlight(f'{svc.gbl.tag}: running ruff')
            toml_path = self._find_ruff_toml()
            cmd = f'ruff check --config {toml_path}'
            svc.utils_ps.run_process(cmd, use_raw_log=True)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tool:"{tool}", use one of: pylint, ruff')

    # --------------------
    ## get location of pylint.rc file.
    # Note: for pylint (python) only
    #
    # @return path to pylint.rc
    def _find_pylintrc(self):
        rc_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'pylint.rc')
        if not os.path.isfile(rc_path):
            rc_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'xplat_utils', 'pylint.rc')
        return rc_path

    # --------------------
    ## get location of ruff.toml file.
    # Note: for ruff (python) only
    #
    # @return path to ruff.toml
    def _find_ruff_toml(self):
        toml_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'ruff.toml')
        if not os.path.isfile(toml_path):
            toml_path = os.path.join(svc.utils_fs.root_dir, 'tools', 'xplat_utils', 'ruff.toml')
        return toml_path

    # --------------------
    ## get list of directories to pylint.
    # Note: for pylint (python) only
    #
    # @return list of directories
    def _get_dirs(self):
        modules = ''
        if svc.cfg.is_module:
            modules += f'{svc.cfg.mod_dir_name} '
        else:
            modules += 'lib '

        files = glob.glob('*.py')
        if files:
            modules += '*.py '

        if svc.cfg.do_lint.include_tools:
            svc.log.line(f'{svc.gbl.tag}: including "tools" directory')
            modules += 'tools '
            path = os.path.join('tools', 'xplat_utils')
            modules += f'{path} '

        # include ver and ut only if the directories exist
        if os.path.isdir('ver'):
            modules += 'ver '
        if os.path.isdir('ut'):
            modules += 'ut '

        return modules

    # --------------------
    ## run cppcheck or clang-tidy
    #
    # @param tool  which lint tool to use: clang-tidy(default), cppcheck
    # @return None
    def _run_cpp(self, tool):
        if tool == 'clang-tidy':
            self._run_cpp_clang_tidy()
        elif tool == 'cppcheck':
            self._run_cpp_check()
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tool:"{tool}", use one of: clang-tidy, cppcheck')

    # --------------------
    ## run cppcheck
    #
    # @return None
    def _run_cpp_check(self):
        modules = ''
        # location of source files being covered
        for src_dir in svc.cfg.do_lint.src_dirs:
            modules += f'{src_dir} '  # pylint: disable=consider-using-join

        svc.log.highlight(f'{svc.gbl.tag}: run cppcheck on: {modules}')
        cmd = 'cppcheck '
        cmd += '--enable=all '
        cmd += '--quiet '  # _                 no progress lines
        cmd += '--inconclusive  '  # _         report errors even if inconclusive
        cmd += '--max-ctu-depth=5 '  # _       minimize max-cross-translation unit checks
        # cmd += '--language=c++ ' # _         not needed
        cmd += '--inline-suppr '  # _          allow inline suppression e.g "// cppcheck-suppress unusedFunction"
        cmd += '--suppress=checkersReport '  # suppress comment to gen checkers report
        if svc.cfg.mod_tech == 'arduino':
            cmd += '--platform=avr8 '  # _     arduino uses avr8 compiler
        else:
            cmd += '--platform=native '  # _   use native compiler spec
        cmd += '--suppress=missingIncludeSystem '  # ignore warnings in system includes
        cmd += '--suppress=functionStatic '  # _     functions can be non-static
        cmd += f'-I {svc.cfg.cpip.root_dir} '
        for path in modules.split(' '):
            path = path.strip()
            if path:
                cmd += f'-I {path} '
        cmd += modules
        # uncomment to debug
        # svc.log.dbg(f'cmd: {cmd}')
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cppcheck rc={svc.gbl.rc}')

    # --------------------
    ## run clang-tidy
    #
    # @return None
    def _run_cpp_clang_tidy(self):
        # skip regen for Makefile projects
        # TODO delete when cmake is deprecated
        if os.path.isfile('CMakeLists.txt'):
            svc.log.highlight(f'{svc.gbl.tag}: cmake refresh compile_commands')
            cmd = 'cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON cmake-build-debug/'
            svc.utils_ps.run_process(cmd, use_raw_log=False)
            svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: compile_commands rc={svc.gbl.rc}')

        modules = ''
        # location of source files being covered
        for src_dir in svc.cfg.do_lint.src_dirs:
            modules += f'{src_dir}/* '  # pylint: disable=consider-using-join

        svc.log.highlight(f'{svc.gbl.tag}: run clang-tidy on: {modules}')
        cmd = 'clang-tidy '
        if os.path.isfile('CMakeLists.txt'):
            cmd += '-p=cmake-build-debug/compile_commands.json '  # TODO delete when cmake is deprecated
        cmd += '--quiet '
        cmd += '--header-filter=.* '
        cmd += modules
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: clang-tidy rc={svc.gbl.rc}')
