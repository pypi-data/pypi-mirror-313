import glob
import os
import re

from .svc import svc


# --------------------
## perform the do_coverage operation
class DoCoverage:
    # --------------------
    ## do_lint mainline.
    #
    # @param action  the action to take: reset, gen
    # @return None
    def run(self, action):
        svc.log.highlight(f'{svc.gbl.tag}: starting {action}...')

        tech = svc.cfg.mod_tech

        if action not in ['gen', 'reset']:
            svc.gbl.rc += 1
            svc.log.err(f'{svc.gbl.tag}: unknown action:{action}, use one of: reset, gen')
        elif tech not in ['python', 'cpp', 'arduino']:
            svc.gbl.rc += 1
            svc.log.err(f'{svc.gbl.tag}: unknown tech:{tech}, use one of: python, cpp, arduino')
        elif tech == 'python':
            if action == 'reset':
                svc.log.warn(f'{svc.gbl.tag}: {action}: not applicable to python tech, skipping')
            else:
                self._python_gen_coverage()
                self._python_report_summary()
        elif tech in ['cpp', 'arduino']:
            if action == 'reset':
                self._cpp_reset_coverage()
            else:  # gen
                self._cpp_gen_coverage()

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: tech:{tech} action:{action} rc={svc.gbl.rc}')

    # --------------------
    ## generate coverage from pylint
    #
    # @return None
    def _python_gen_coverage(self):
        cmd = 'coverage html --rcfile setup.cfg'
        rc, out = svc.utils_ps.run_cmd(cmd)
        svc.gbl.rc += rc
        svc.log.line(f'{svc.gbl.tag}: {out}')

    # --------------------
    ## report on current coverage values
    # assumes: index.html has a known format
    #
    # @return None
    def _python_report_summary(self):
        path = os.path.join(svc.gbl.outdir, 'coverage', 'index.html')
        with open(path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()

            names = ['statements', 'missing', 'excluded', 'branches', 'partial', 'coverage']
            in_details = False
            detail_num = 0
            for line in lines:
                m = re.search(r'class="pc_cov">(.*)<', line)
                if m:
                    svc.log.line(f'{svc.gbl.tag}: Total: {m.group(1)}')
                    continue

                if not in_details:
                    m = re.search(r'<tfoot>', line)
                    if m:
                        in_details = True
                        detail_num = 0
                else:
                    m = re.search(r'<td>(\d+)</td>', line)
                    if m:
                        svc.log.line(f'{svc.gbl.tag}:    {names[detail_num]: <10}: {m.group(1): >5}')
                        detail_num += 1

    # --------------------
    ## reset gcov counters by deleting cmake-build-debug/*.gcda files
    # Note: if you delete .gcno => you have to recreate cmake-build-debug
    def _cpp_reset_coverage(self):
        path = 'cmake-build-debug'
        files = glob.glob(f'{path}/**/*.gcda', recursive=True)
        for file in files:
            svc.utils_fs.safe_delete_file(file, verbose=False)

    # --------------------
    ## generate coverage using gcovr.
    # see https://gcovr.com/en/4.2/guide.html
    # * Note: gcovr --gcov-executable gcov-8
    # * Note: gcovr --gcov-executable "llvm-cov gcov" # For CLANG
    #
    # @return None
    def _cpp_gen_coverage(self):
        covdir = f'{svc.gbl.outdir}/coverage'
        svc.utils_fs.clean_out_dir('coverage', verbose=False)

        report_page = f'{covdir}/ut.html'

        cmd = ('gcovr --html-details '  # show individual source files
               '-r cmake-build-debug '  # default to debug for unit test coverage
               '--sort=uncovered-percent '  # sort source files based on percentage uncovered lines
               '--print-summary '  # print summary to stdout
               f'-o {report_page} '  # location of report main page
               )

        # all directories named in xplat.do_ut
        for cov_dir in svc.cfg.do_ut.cov_dirs:
            cmd += f'--filter {cov_dir} '  # location of source files being covered

        svc.log.line(f'{svc.gbl.tag}: summary report:')
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.line(f'{svc.gbl.tag}: report is located in: {report_page}')
