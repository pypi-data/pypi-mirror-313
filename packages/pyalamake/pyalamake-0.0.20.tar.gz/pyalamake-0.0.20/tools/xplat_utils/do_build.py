import os

from .do_cpip import DoCpip
from .svc import svc


# --------------------
## perform the do_lint operation
class DoBuild:
    # --------------------
    ## do_build mainline.
    #
    # @param tech        technology: cpp, arduino
    # @param build_type  build type: debug or release
    # @param target      cmake target to build e.g. ut
    # @return None
    def run(self, tech, build_type, target):
        if not build_type:
            build_type = 'debug'

        if build_type not in ['debug', 'release']:
            svc.gbl.rc += 1
            svc.log.err(f'unknown build_type:{build_type}, use one of: debug, release')

        if not tech:
            # default to xplat.cfg value
            tech = svc.cfg.mod_tech
        if not tech:
            # not set, the default to cpp
            tech = 'cpp'

        if not target:
            target = svc.cfg.mod_name

        svc.log.highlight(f'{svc.gbl.tag}: starting tech:{tech} target:{target}...')

        # generate CPIP files as needed
        cpip = DoCpip()
        cpip.gen()

        if tech in ['cpp']:
            self._run_cpp(build_type, target)
        elif tech in ['arduino']:
            self._run_arduino(build_type, target)
        else:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tech:{tech}, use one of: python, cpp, arduino')

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: build {build_type} rc={svc.gbl.rc}')

    # --------------------
    ## build a cpp app or library
    #
    # @param build_type  build type: debug or release
    # @param target      the cmake target to build e.g. ut
    # @return None
    def _run_cpp(self, build_type, target):
        build_dir = f'cmake-build-{build_type}'
        if not os.path.isdir(build_dir):
            svc.utils_fs.safe_create_dir(build_dir)
            if build_type == 'debug':
                btype = 'Debug'
            else:
                btype = 'Release'
            svc.log.line(f'{svc.gbl.tag}: load project for {build_type}')
            cmd = f'cmake -DCMAKE_BUILD_TYPE={btype} -DCMAKE_MAKE_PROGRAM=ninja -G Ninja -S . -B {build_dir}'
            svc.utils_ps.run_process(cmd, use_raw_log=False)
            svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cmake load proj. {build_type} rc={svc.gbl.rc}')

        svc.log.line(f'{svc.gbl.tag}: update makefile')
        cmd = f'cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON {build_dir}/'
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cmake makefile {build_type} rc={svc.gbl.rc}')

        if svc.gbl.rc != 0:
            return

        svc.log.line(f'{svc.gbl.tag}: build {build_type} target:{target}')
        cmd = f'cmake --build {build_dir} --target {target} -j 6'
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cmake build {build_type} rc={svc.gbl.rc}')

    # --------------------
    ## build an arduino binary image
    #
    # @param build_type  build type: debug or release
    # @param target      the cmake target to build
    # @return None
    def _run_arduino(self, build_type, target):
        svc.log.line(f'{svc.gbl.tag}: build {build_type} target:{target}')
        if target == 'ut':
            make_parm = 'ut_build'
        else:
            make_parm = f'build-{build_type}'
        cmd = f'make {make_parm}'
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: arduino {make_parm} rc={svc.gbl.rc}')
