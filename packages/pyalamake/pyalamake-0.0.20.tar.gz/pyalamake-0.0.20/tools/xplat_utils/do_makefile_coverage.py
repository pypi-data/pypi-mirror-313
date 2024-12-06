from .svc import svc


# --------------------
## perform the do_coverage operations for Makefile based projects
class DoMakefileCoverage:
    # --------------------
    ## do_makefile_coverage mainline.
    #
    # @param action  the action to take: reset, gen
    # @param target  the makefile target name
    # @return None
    def run(self, action, target):
        svc.log.highlight(f'{svc.gbl.tag}: starting {action} for target: {target}...')

        if action == 'reset':
            self._cpp_reset_coverage(target)
        elif action == 'gen':
            self._cpp_gen_coverage(target)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown action:{action}, use one of: reset, gen')

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: action:{action} rc={svc.gbl.rc}')

    # --------------------
    ## reset gcov counters by deleting debug/*.gcda files
    #
    # @param target  the target to generate the coverage for
    # @return None
    def _cpp_reset_coverage(self, target):
        cmd = f'make {target}-cov-reset'
        svc.utils_ps.run_process(cmd)

    # --------------------
    ## generate coverage using gcovr.
    # see https://gcovr.com/en/4.2/guide.html
    # * Note: gcovr --gcov-executable gcov-8
    # * Note: gcovr --gcov-executable "llvm-cov gcov" # For CLANG
    #
    # @param target  the target to generate the coverage for
    # @return None
    def _cpp_gen_coverage(self, target):
        cmd = f'make {target}-cov'
        svc.utils_ps.run_process(cmd)
