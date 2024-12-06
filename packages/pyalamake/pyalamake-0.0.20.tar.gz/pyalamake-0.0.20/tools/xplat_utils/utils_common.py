import os
import typing

from .svc import svc


# ---------------------
## common functions;
class UtilsCommon:
    # ---------------------
    ## get the top directory of src files.
    # aborts if the directory does not exist
    #
    # @param tag     for logging purposes
    # @param subdir  optional subdirectory
    # @return the relative directory path to the source
    @staticmethod
    def get_src_dir(tag, subdir) -> typing.Optional[str]:
        path = ''
        if svc.cfg.mod_tech in ['python']:
            if svc.cfg.is_module:
                mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
                if subdir:
                    path = os.path.join(str(mod_dir), 'lib', subdir)
                else:
                    path = os.path.join(str(mod_dir), 'lib')
            else:
                if subdir:
                    path = os.path.join(svc.utils_fs.root_dir, 'lib', subdir)
                else:
                    path = os.path.join(svc.utils_fs.root_dir, 'lib')
        elif svc.cfg.mod_tech in ['cpp', 'arduino']:
            if svc.cfg.is_module:
                if subdir:
                    path = os.path.join(svc.utils_fs.root_dir, 'lib', subdir)
                else:
                    path = os.path.join(svc.utils_fs.root_dir, 'lib')
            else:
                if subdir:
                    path = os.path.join(svc.utils_fs.root_dir, 'src', subdir)
                else:
                    path = os.path.join(svc.utils_fs.root_dir, 'src')
        else:
            svc.gbl.rc = 1
            svc.abort(f'{tag}: unknown tech: {svc.cfg.mod_tech}')  # okay to abort; tech should always be defined

        if path and not os.path.isdir(path):
            svc.gbl.rc = 1
            svc.abort(f'{tag}: dir does not exist: {path}')  # okay to abort; directory should always exist

        # uncomment to debug
        # print(f'DBG @@@ {tag} path:{path}')

        return str(path)

    # --------------------
    ## return the module name for this given arg
    #  if var is invalid, AttributeError is thrown
    #
    # @param var   the variable to retrieve
    # @return the module name or an error message
    @staticmethod
    def get_cfg(var):
        return getattr(svc.cfg, var)

    # --------------------
    ## return the Coverage options needed for the module/app.
    # note: these are for python only; see do_coverage for cpp and other techs
    #
    # @return coverage options needed for pytest (python)
    @staticmethod
    def get_cov_opts():
        opts = ''
        # the directory to cover
        if svc.cfg.is_module:
            opts += f'--cov={svc.cfg.mod_dir_name}/lib '
        else:  # an app
            opts += '--cov=lib '

        opts += '--cov-report= '  # the type of report; default is HTML
        opts += '--cov-branch '  # branch coverage
        opts += '--cov-config=setup.cfg '  # other cfg is in setup.cfg
        opts += '--cov-append'  # append to coverage content; up to caller to clear it
        return opts
