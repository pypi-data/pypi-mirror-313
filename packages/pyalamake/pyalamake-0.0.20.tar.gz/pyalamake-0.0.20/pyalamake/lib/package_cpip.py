import os

from .svc import svc


# --------------------
## handle CPIP packages
class PackageCpip:
    # --------------------
    ## find the CPIP package name and return info for it
    #
    # @param pkgname  the CPIP package to search for
    # @return the package info
    def find(self, pkgname):
        pkgname = pkgname.replace('cpip.', '')
        svc.log.line(f'finding cpip package: {pkgname}')

        if not os.path.isdir(os.path.join('tools', 'xplat_utils')):
            svc.abort('xplat_utils is not installed, aborting')

        from tools.xplat_utils import main
        pkginfo = main.svc.utils.cpip_get(pkgname)
        if pkginfo is None:
            svc.abort(f'could not find info for cpip package: {pkgname}')

        return pkginfo
