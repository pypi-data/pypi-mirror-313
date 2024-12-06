import os

from .svc import svc


# --------------------
## perform gen constants operations
class GenConstants:
    # --------------------
    ## generate constant file
    #
    # @param subdir  (optional) subdirectory to place the constants files
    # @return None
    def run(self, subdir):
        if svc.cfg.mod_tech in ['', 'python']:
            self.gen_constants(subdir)
        else:
            svc.log.warn(f'gen_constants: does not work for tech: {svc.cfg.mod_tech}')
            svc.gbl.rc = 1

    # --------------------
    ## generate the constants_version.py file in the module/app directory
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def gen_constants(self, subdir):
        if subdir:
            filedir = os.path.join('lib', subdir)
        else:
            filedir = os.path.join('lib')

        if svc.cfg.is_module:
            mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
            if not os.path.isdir(mod_dir):
                svc.log.warn(f'gen_constants: dir does not exist: {mod_dir}')
                svc.gbl.rc = 1
                return

            path = os.path.join(str(mod_dir), filedir)
        else:
            path = os.path.join(svc.utils_fs.root_dir, filedir)

        path = os.path.join(path, 'constants_version.py')
        # svc.log.dbg(f'path: {path}')

        # generate constants file
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write('from dataclasses import dataclass\n')
            fp.write('\n')
            fp.write('\n')
            fp.write('# --------------------\n')
            fp.write('## holds constants\n')
            fp.write('@dataclass\n')
            fp.write('class ConstantsVersion:\n')
            fp.write('    ## current App version\n')
            fp.write(f'    version = \'{svc.cfg.version}\'\n')

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        msg = f'gen: constants_version.py rc={svc.gbl.rc}'
        if not svc.gbl.verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc
