import glob
import os

from .svc import svc


# --------------------
## perform the do_clean operation
class DoClean:
    # --------------------
    ## do_clean mainline.
    #
    # @param subdir   subdirectory if any
    # @param depth    how much to clean: lite, full;  '' defaults to lite
    # @return None
    def run(self, subdir='', depth=''):
        verbose = 'min'
        if depth == '':
            depth = 'lite'

        svc.log.highlight(f'{svc.gbl.tag}: starting tech:{svc.cfg.mod_tech} '
                          f'module:{svc.cfg.is_module} depth:{depth}...')

        svc.utils_fs.safe_delete_tree(svc.gbl.outdir, verbose=verbose)
        svc.utils_fs.safe_delete_file('Doxyfile', verbose=verbose)
        svc.utils_fs.safe_delete_file('.coverage', verbose=verbose)
        svc.utils_fs.safe_delete_tree('dist', verbose=verbose)
        svc.utils_fs.safe_delete_tree('.pytest_cache', verbose=verbose)

        if svc.cfg.mod_tech in ['python']:
            self._del_python(verbose, subdir)
        elif svc.cfg.mod_tech in ['cpp', 'arduino']:
            self._del_cpp(verbose, subdir)

        if depth == 'full':
            svc.utils_fs.safe_delete_tree('venv', verbose=verbose)

            # must be after venv
            self._delete_cache(verbose)

        # note: no return code

    # --------------------
    ## delete python specific directories and files
    #
    # @param verbose  the logging verbosity
    # @param subdir   the subdirectory in the source root directory
    # @return None
    def _del_python(self, verbose, subdir):
        if svc.cfg.is_module:
            if subdir:
                filedir = os.path.join(svc.cfg.mod_dir_name, 'lib', subdir)
            else:
                filedir = os.path.join(svc.cfg.mod_dir_name, 'lib')
        else:
            if subdir:
                filedir = os.path.join('lib', subdir)
            else:
                filedir = os.path.join('lib')

        if svc.cfg.is_module:
            svc.utils_fs.safe_delete_tree(os.path.join(f'{svc.cfg.mod_dir_name}.egg-info'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join('setup.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join('MANIFEST.in'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join(filedir, 'build_info.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join(filedir, 'version.json'), verbose=verbose)
            # don't delete constants_version.py
        else:  # an app
            svc.utils_fs.safe_delete_file(os.path.join(filedir, 'build_info.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join(filedir, 'version.json'), verbose=verbose)
            # don't delete constants_version.py

    # --------------------
    ## delete cpp specific directories and files
    #
    # @param verbose  the logging verbosity
    # @param subdir   the subdirectory in the source root directory
    # @return None
    def _del_cpp(self, verbose, subdir):
        svc.utils_fs.safe_delete_tree('cmake-build-debug', verbose=verbose)
        svc.utils_fs.safe_delete_tree('cmake-build-release', verbose=verbose)
        svc.utils_fs.safe_delete_tree('debug', verbose=verbose)
        svc.utils_fs.safe_delete_tree('release', verbose=verbose)

        if svc.cfg.is_module:
            if subdir:
                filedir = os.path.join('lib', subdir)
            else:
                filedir = os.path.join('lib')
        else:
            if subdir:
                filedir = os.path.join('src', subdir)
            else:
                filedir = os.path.join('src')

        svc.utils_fs.safe_delete_file(os.path.join(filedir, 'build_info.txt'), verbose=verbose)
        # don't delete version.h

    # --------------------
    ## recursively deletes __pycache__ subdirectories in the root_dir.
    #
    # @param verbose  logging verbosity: 'full' or ''
    # @return None
    def _delete_cache(self, verbose):
        folders = glob.glob('**/__pycache__', recursive=True)
        # uncomment to debug
        # svc.log.dbg(f'{folders}')

        if not folders:
            return

        # at least one cache folder exists
        for folder in folders:
            # uncomment to debug
            # svc.log.dbg(f'rmtree {folder}')
            if folder.startswith('./venv'):
                continue
            svc.utils_fs.safe_delete_tree(folder, verbose=verbose)
