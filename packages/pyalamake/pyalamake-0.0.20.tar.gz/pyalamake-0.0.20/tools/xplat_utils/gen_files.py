import json
import os

from .gen_build_info import GenBuildInfo
from .gen_constants import GenConstants
from .svc import svc


# --------------------
## perform gen files operations
class GenFiles:
    # --------------------
    ## generate all files
    #
    # @param dogen    ''      => no files
    #                 'dogen' => python : gen version.json and build_info.py
    #                 'dogen' => cpp,ard: gen version.h and build_info.txt
    #                 'dogen1'=> python : gen version.py
    #                 'dogen1'=> cpp,ard: gen version.h
    #                 'dogen2'=> python: gen version.py and build_info.py
    #                 'dogen2'=> cpp   : gen version.h and build_info.txt
    # @param subdir  (optional) subdirectory to place the files
    # @return None
    def all(self, dogen='', subdir=''):
        if svc.cfg.mod_tech not in ['python', 'cpp', 'arduino']:
            svc.gbl.rc += 1
            svc.log.err(f'unknown tech:{svc.cfg.mod_tech}, use one of: python, cpp or arduino')
        elif dogen not in ['', 'dogen', 'gen_both', 'gen_constants', 'gen_build_info']:
            svc.gbl.rc += 1
            svc.log.err(f'unknown dogen:{dogen}, use one of: "" or gen_both, gen_constants, gen_build_info')
        elif dogen in ['', 'dogen']:
            self._do_gen(subdir)
        elif dogen == 'gen_both':
            self._do_gen_both(subdir)
        elif dogen == 'gen_constants':
            self._do_gen_constants(subdir)
        else:  # dogen == 'gen_build_info':
            self._do_gen_build_info(subdir)

    # --------------------
    ## run do_gen option
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _do_gen(self, subdir):
        if svc.cfg.mod_tech == 'python':
            self._version_json(subdir)
        else:  # svc.cfg.mod_tech in ['cpp', 'arduino']
            self._version_h(subdir)
        self._do_gen_build_info(subdir)

    # --------------------
    ## run gen_both option
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _do_gen_both(self, subdir):
        self._do_gen_constants(subdir)
        self._do_gen_build_info(subdir)

    # --------------------
    ## run gen_constants option
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _do_gen_constants(self, subdir):
        if svc.cfg.mod_tech == 'python':
            impl = GenConstants()
            impl.run(subdir)
        else:  # svc.cfg.mod_tech in ['cpp', 'arduino']
            self._version_h(subdir)

    # --------------------
    ## run gen_build_info option
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _do_gen_build_info(self, subdir):
        if svc.cfg.mod_tech == 'python':
            self._build_info_file(subdir)
        else:  # svc.cfg.mod_tech in ['cpp', 'arduino']
            self._build_info_txt(subdir)

    # --------------------
    ## generate the version.json file in the module/app directory
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _version_json(self, subdir):
        fname = 'version.json'
        path = os.path.join(svc.utils.get_src_dir('version_json', subdir), fname)

        version = {'version': svc.cfg.version}
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            json.dump(version, fp, indent=4)

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        self._report_rc(fname)

    # ---------------------
    ## generate version.h for cpp/arduino
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _version_h(self, subdir):  # pylint: disable=unused-argument
        fname = 'version.h'
        path = os.path.join(svc.utils.get_src_dir('version_h', subdir), fname)

        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write('#ifndef VERSION_H\n')
            fp.write('#define VERSION_H\n')
            fp.write(f'static const char version[] = "{svc.cfg.version}";\n')
            fp.write('#endif //VERSION_H\n')

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        self._report_rc(fname)

    # --------------------
    ## generate the build_info.py file in the module/app source directory
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _build_info_file(self, subdir):
        fname = 'build_info.py'
        path = os.path.join(svc.utils.get_src_dir('build_info_file', subdir), fname)
        self._gen_build_info(path)
        self._report_rc(fname)

    # ---------------------
    ## generate build_info.txt file
    #
    # @param subdir the subdirectory in the source root directory
    # @return None
    def _build_info_txt(self, subdir):
        fname = 'build_info.txt'
        path = os.path.join(svc.utils.get_src_dir('build_info_txt', subdir), fname)
        self._gen_build_info(path)
        self._report_rc(fname)

    # ---------------------
    ## generate build_info file at the given path
    #
    # @param path the location to gen the file into
    # @return None
    def _gen_build_info(self, path):
        binfo = GenBuildInfo()
        binfo.init(path)
        svc.gbl.rc = binfo.gen(svc.cfg.version)
        binfo.term()

    # ---------------------
    ## report rc to generate given filename
    #
    # @param fname  the file generated
    # @return None
    def _report_rc(self, fname):
        msg = f'gen: {fname} rc={svc.gbl.rc}'
        if not svc.gbl.verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc
