from .svc import svc


# --------------------
## perform the do_makefile operations
class DoMakefile:
    # --------------------
    ## do_build mainline.
    #
    # @param target      cmake target to build e.g. ut
    # @return None
    def run(self, target):
        svc.log.highlight(f'{svc.gbl.tag}: starting target:{target}...')
        self._run_make(target)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: target {target} rc={svc.gbl.rc}')

    # --------------------
    ## run a makefile target
    #
    # @param target      the make target to run e.g. ut
    # @return None
    def _run_make(self, target):
        cmd = f'make {target}'
        svc.utils_ps.run_process(cmd)
