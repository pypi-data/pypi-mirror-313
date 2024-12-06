import json
import os

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## perform the do_ver_info operation
class DoVerInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## the list of versions tested so far
        self._test_versions = {}

    # --------------------
    ## do_ver_info mainline.
    #
    # @return None
    def run(self):
        svc.log.highlight(f'{svc.gbl.tag}: starting save...')

        self._gen_version_info()
        self._gen_markdown()

    # --------------------
    ## generate or udpate version info json file
    #
    # @return None
    def _gen_version_info(self):
        svc.log.line(f'{svc.gbl.tag}: generating version_info')

        # this location is hardcoded
        path = os.path.join('tools', 'version_info.json')

        if os.path.isfile(path):
            # load existing data
            with open(path, 'r', encoding='utf-8') as fp:
                self._test_versions = json.load(fp)
        else:
            # first time generating the file
            # Note: these must match the tags in OsSpecific
            self._test_versions = {
                'ubuntu': {},
                'win': {},
                'macos': {},
                'rpi': {},
            }

        # get version info
        info = f'{OsSpecific.os_version}, {OsSpecific.python_version}'
        self._test_versions[OsSpecific.os_name][info] = 1

        # save it
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            json.dump(self._test_versions, fp, indent=4)

    # --------------------
    ##  generates the markdown file
    def _gen_markdown(self):
        svc.log.line(f'{svc.gbl.tag}: generating markdown')

        # TODO get location from .cfg
        # generate list of versions for each platform
        path = os.path.join('doc', 'version_info.md')
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            for platform in sorted(self._test_versions.keys()):
                for version in sorted(self._test_versions[platform].keys()):
                    fp.write(f'{version}\n')
