import os
import re
import shutil
from pathlib import Path

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## holds all file system related utility functions
class UtilsFs:
    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()
        ## holds the root directory for all files and directories
        self._root_dir = None

    # --------------------
    ## convert path to appropriate slash for the OS
    #
    # @param path  the path to convert
    # @return the convert path
    def slash_convert(self, path):
        if OsSpecific.os_name == 'win':
            return path.replace('/', '\\')
        return path.replace('\\', '/')

    # --------------------
    ## convert path with leading C:\ to msys2 compatible
    #
    # @param path  the path to convert
    # @return the convert path
    def full_convert(self, path):
        if OsSpecific.os_name == 'win':
            path = path.replace('\\', '/')
            path = path.replace('//', '/')
            m = re.search(r'^(.):/(.*)', path)
            if m:
                path = f'/{m.group(1)}/{m.group(2)}'

        return path

    # --------------------
    ## returns the root directory whether in a module in venv or locally
    #
    # @return the root dir
    @property
    def root_dir(self):
        if self._root_dir is None:
            self._root_dir = str(Path('..').parent)

        return self._root_dir

    # --------------------
    ## create the out directory.
    # return the outdir as an absolute path
    #
    # @return the module name or an error message
    def create_outdir(self):
        path = self.convert_relative_to_abs(svc.gbl.outdir)
        self.safe_create_dir(path)
        return str(path)

    # --------------------
    ## convert a relative path to an absolute path, e.g.
    # * ~/out    => /home/xx/out
    # * ./out    => /home/xx/projects/proj1/out
    # * out      => /home/xx/projects/proj1/out
    #
    # @param path  the path to convert
    # @return the converted path
    def convert_relative_to_abs(self, path):
        path1 = os.path.expanduser(path)
        path2 = os.path.abspath(path1)
        return path2

    # --------------------
    ## delete and then recreate the given subdirectory in "${OUT_DIR}"
    #
    # @param dst      the subdirectory to delete and recreate
    # @param verbose  logging verbosity
    # @return None
    def clean_out_dir(self, dst, verbose='quiet'):
        path1 = self.convert_relative_to_abs(svc.gbl.outdir)
        path = os.path.join(path1, dst)
        self.safe_delete_tree(path, verbose)
        self.safe_create_dir(path)

    # --------------------
    ## deletes a file in the given path in the root directory
    #
    # @param dst_path  the file to delete
    # @param verbose  logging verbosity
    # @return None
    def safe_delete_file(self, dst_path, verbose='quiet'):
        path = os.path.join(self.root_dir, dst_path)

        if not os.path.isfile(path):
            if verbose in ['full']:
                svc.log.ok(f'{"rm: file does not exist": <25}: {path}')
            return

        try:
            # uncomment to debug
            # svc.log.dbg(f'rm file: {path}')
            os.remove(path)
            if verbose in ['full', 'min']:
                svc.log.ok(f'{"rm: file ": <25}: {path}')
        except OSError as excp:  # pragma: no cover
            # coverage: needs sudo access to cause a delete failure
            svc.log.err(f'{"failed to delete file": <25}: {excp.filename}, {excp.strerror}')
            svc.gbl.rc += 1

    # --------------------
    ## deletes a sub-directory in the root dir
    #
    # @param dst_path  the subdirectory to delete
    # @param verbose  logging verbosity
    # @return None
    def safe_delete_tree(self, dst_path, verbose='quiet'):
        path = os.path.join(self.root_dir, dst_path)

        if not os.path.isdir(path):
            if verbose in ['full']:
                svc.log.ok(f'{"rm: dir  does not exist": <25}: {path}')
            return

        try:
            shutil.rmtree(path)
            if verbose in ['full', 'min']:
                svc.log.ok(f'{"rm: dir": <25}: {path}')
        except OSError as excp:  # pragma: no cover
            # coverage: needs sudo access to cause a delete failure
            svc.log.err(f'{"failed to delete dir": <25}: {excp.filename}, {excp.strerror}')
            svc.gbl.rc += 1

    # --------------------
    ## create the given subdirectory if not already existing
    #
    # @param dst   the subdirectory to create
    # @return None
    def safe_create_dir(self, dst):
        path = os.path.join(self.root_dir, dst)
        os.makedirs(path, exist_ok=True)

    # --------------------
    ## create the given global directory if not already existing
    #
    # @param path   the directory to create
    # @return None
    def safe_global_dir(self, path):
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            svc.log.ok(f'already exists: {path}')
            return

        Path(path).mkdir(parents=True, exist_ok=True)
        if os.path.isdir(path):
            svc.log.ok(f'created: {path}')
        else:  # pragma: no cover
            # coverage: needs sudo access to cause a delete failure
            svc.log.err(f'failed to mkdir: {path}')

    # --------------------
    ## create the file from src to the dst_dir with the new file name
    #
    # @param src        the full path to the file to copy
    # @param dst_dir    the directory to copy to
    # @param dst_file   the new name of the file
    # @return None
    def safe_copy_file(self, src, dst_dir, dst_file):
        dst_dir = os.path.expanduser(dst_dir)
        if not os.path.isdir(dst_dir):
            svc.log.err(f'cannot find: {dst_dir}')
            svc.gbl.rc += 1
            return

        dst = os.path.join(dst_dir, dst_file)
        shutil.copyfile(src, dst)
