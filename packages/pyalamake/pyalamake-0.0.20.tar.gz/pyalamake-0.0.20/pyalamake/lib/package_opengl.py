from dataclasses import dataclass

from .svc import svc


# --------------------
## info for the OpenGL package
class PackageOpengl:
    # --------------------
    ## return info about the pkgname
    #
    # @param pkgname  the name of the package; default: opengl
    # @return ref to OpenGl info
    def find(self, pkgname):
        svc.log.line(f'finding package: {pkgname}')

        @dataclass
        class OpenGl:
            include_dir = '/usr/include'
            link_libs = ['glut', 'GLU', 'GL']

        return OpenGl
