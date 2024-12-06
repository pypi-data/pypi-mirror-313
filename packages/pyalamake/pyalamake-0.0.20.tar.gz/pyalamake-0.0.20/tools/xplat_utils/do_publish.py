import os
import re

from .svc import svc


# --------------------
## perform the do_clean operation
class DoPublish:
    # --------------------
    ## do_publish mainline.
    #
    # @return None
    def run(self):
        # script also prints this; comment out for now
        # log.highlight(f'{svc.glbl.tag} starting...')
        svc.gbl.rc = 0

        if svc.cfg.mod_name in svc.cfg.do_publish.disallow:
            svc.log.warn(f'cannot publish; disallowed by: {svc.cfg.do_publish.disallow}')
            svc.gbl.rc = 1
            return

        if not svc.cfg.is_module:
            svc.log.warn('do_publish is only functional for modules')

        self._gen_setup_py()
        self._gen_manifest_in()

    # --------------------
    ## generate setup.py file
    #
    # @return None
    def _gen_setup_py(self):
        svc.utils_fs.safe_delete_file('setup.py')

        # generate the setup.py file from setup_template.py
        src = os.path.join(svc.utils_fs.root_dir, 'tools', 'setup_template.py')
        dst = os.path.join(svc.utils_fs.root_dir, 'setup.py')
        with open(dst, 'w', encoding='utf-8', newline='\n') as fp_dst:
            with open(src, 'r', encoding='utf-8') as fp_src:
                for line in fp_src:
                    while True:
                        m = re.search(r'\$\$([^$]+)\$\$', line)
                        if not m:
                            # uncomment to debug
                            # log.dbg(f'line: {line.rstrip()}')
                            fp_dst.write(line)
                            break

                        vrbl = m.group(1)
                        if vrbl == 'root_dir':
                            val = str(svc.utils_fs.root_dir)
                        else:
                            val = getattr(svc.cfg, vrbl)
                        # uncomment to debug
                        # log.dbg(f'grp:{m.group(1)} line:{line.strip()}')
                        line = line.replace(f'$${vrbl}$$', val)

    # --------------------
    ## generate manifest file
    #
    # @return None
    def _gen_manifest_in(self):
        fname = 'MANIFEST.in'
        svc.utils_fs.safe_delete_file(fname)
        dst = os.path.join(svc.utils_fs.root_dir, fname)
        with open(dst, 'w', encoding='utf-8', newline='\n') as fp:
            # graft module_name
            # global-exclude *.py[cod]
            fp.write(f'graft {svc.cfg.mod_dir_name}\n')
            fp.write('global-exclude *.py[cod]\n')
