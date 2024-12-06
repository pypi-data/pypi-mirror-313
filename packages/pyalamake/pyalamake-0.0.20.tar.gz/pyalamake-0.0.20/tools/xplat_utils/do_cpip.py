import json
import os
import shutil
from dataclasses import dataclass

import requests
import urllib3

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## perform the do_publish using cpip operation.
class DoCpip:
    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        ## location of the staging local directory
        self._staging_dir = 'staging'
        ## the location of the cpip directory (may have ~ in it)
        self._cpip_root_dir = self._convert(os.path.expanduser(svc.cfg.cpip.root_dir))
        ## the location of the cpip.json file
        self._cpip_json = os.path.join(self._cpip_root_dir, 'cpip.json')

    # --------------------
    ## do_cpip mainline
    #
    # @param action  the action to take: pull or publish
    # @return None
    def run(self, action):
        svc.log.highlight(f'{svc.gbl.tag}: starting cpip: {action} ...')

        # make sure root dir and cpip.json exists
        self._check_cpip_info_exists()

        if action == 'publish':
            self._do_staging()
            self._publish_to_local()
        elif action == 'pull':
            self._pull_remote_to_local()
        else:
            svc.abort(f'{svc.gbl.tag}: action is invalid: {action}, expected publish or pull')

    # === publish functions

    # --------------------
    ## stage all content ready for a push
    #
    # @return None
    def _do_staging(self):
        svc.log.highlight(f'{svc.gbl.tag}: staging content for push...')
        cpip_json = self._get_cpip_json()

        svc.utils_fs.safe_delete_tree(self._staging_dir)
        svc.utils_fs.safe_create_dir(self._staging_dir)

        # content for staging/cpip.json
        cpip_publish_json = self._get_cpip_publish_json()
        # uncomment to debug
        # svc.log.dbg(f'{svc.gbl.tag}: cpip_json: {json.dumps(cpip_json, indent=4)}')

        for pkg, pkg_data in cpip_publish_json.items():
            if pkg not in cpip_json:
                # new package
                cpip_json[pkg] = {
                    'desc': 'unset',
                    'src-proj': 'unset',
                    'deleted': False,
                    'platforms': [],
                    'src': [],
                    'dst': 'unset',
                }

            self._handle_pkg_desc(pkg, pkg_data, cpip_json[pkg])
            self._handle_src_proj(pkg, pkg_data, cpip_json[pkg])
            self._handle_deleted(pkg, pkg_data, cpip_json[pkg])
            self._handle_platforms(pkg, pkg_data, cpip_json[pkg])
            self._handle_src_dst(pkg, pkg_data, cpip_json[pkg])
            if 'lib.src' in pkg_data:
                svc.log.warn(f'{svc.gbl.tag}: {pkg}: ignoring "lib.src" in cpip_publish.json, not used')

        # uncomment to debug
        # svc.log.dbg(f'{svc.gbl.tag}: cpip_json: {json.dumps(cpip_json, indent=4)}')

        # save the updated cpip.json file
        path = os.path.join(self._staging_dir, 'cpip.json')
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(cpip_json, fp, indent=4)

    # --------------------
    ## handle desc field in cpip_publish.json
    #
    # @param pkg        the current package
    # @param pkg_data   content of cpip_publish.json
    # @param cpip_pkg   content of cpip.json for current package
    # @return None
    def _handle_pkg_desc(self, pkg, pkg_data, cpip_pkg):
        if 'desc' in pkg_data:
            cpip_pkg['desc'] = pkg_data['desc']
        elif cpip_pkg['desc'] == 'unset':
            svc.log.warn(f'{svc.gbl.tag}: {pkg}: "desc" is not set in cpip_publish.json or cpip.json')

    # --------------------
    ## handle src-proj field in cpip_publish.json
    #
    # @param pkg        the current package
    # @param pkg_data   content of cpip_publish.json
    # @param cpip_pkg   content of cpip.json for current package
    # @return None
    def _handle_src_proj(self, pkg, pkg_data, cpip_pkg):
        if 'src-proj' in pkg_data:
            svc.log.warn(f'{svc.gbl.tag}: {pkg}: ignoring "src_proj" in cpip_publish.json, using: {svc.cfg.mod_name}')
        cpip_pkg['src-proj'] = svc.cfg.mod_name

    # --------------------
    ## handle deleted field in cpip_publish.json
    #
    # @param pkg        the current package
    # @param pkg_data   content of cpip_publish.json
    # @param cpip_pkg   content of cpip.json for current package
    # @return None
    def _handle_deleted(self, pkg, pkg_data, cpip_pkg):
        if 'deleted' not in pkg_data:
            return

        if not isinstance(pkg_data['deleted'], bool):
            svc.abort(f'{svc.gbl.tag}: {pkg}: "deleted" should be boolean, actual: {type(pkg_data["deleted"])}')

        cpip_pkg['deleted'] = pkg_data['deleted']

    # --------------------
    ## handle platforms field in cpip_publish.json
    #
    # @param pkg        the current package
    # @param pkg_data   content of cpip_publish.json
    # @param cpip_pkg   content of cpip.json for current package
    # @return None
    def _handle_platforms(self, pkg, pkg_data, cpip_pkg):
        if 'platforms' in pkg_data:
            cpip_pfs = cpip_pkg['platforms']
            pkg_pfs = pkg_data['platforms']
            if pkg_pfs != cpip_pfs:
                svc.log.line(f'{svc.gbl.tag}: {pkg}: platforms updated to: {pkg_pfs} from {cpip_pfs}')
                cpip_pkg['platforms'] = pkg_pfs
        elif OsSpecific.os_name not in cpip_pkg['platforms']:
            # platforms doesn't exist in cpip_publish and this platform isn't in there already, so add it
            cpip_pkg['platforms'].append(OsSpecific.os_name)

    # --------------------
    ## handle src and dst fields in cpip_publish.json
    #
    # @param pkg        the current package
    # @param pkg_data   content of cpip_publish.json
    # @param cpip_pkg   content of cpip.json for current package
    # @return None
    def _handle_src_dst(self, pkg, pkg_data, cpip_pkg):
        if 'src' not in pkg_data and 'dst' not in pkg_data:
            # nothing to do
            return

        if 'src' in pkg_data and 'dst' in pkg_data:
            cpip_pkg['dst'] = pkg_data['dst'].replace('{os-name}', OsSpecific.os_name)
            cpip_pkg['src'] = []
            src_pattern = pkg_data['src']
            for curr_file in pkg_data['paths']:
                file_name = os.path.basename(curr_file)
                src_path = src_pattern.replace('{file}', file_name)
                src_path = src_path.replace('{os-name}', OsSpecific.os_name)
                src_path = self._convert(src_path)
                src_file = os.path.basename(src_path)

                stg_dir = os.path.join(self._staging_dir, pkg_data['dst'], src_path)
                stg_dir = stg_dir.replace('{os-name}', OsSpecific.os_name)
                stg_dir = self._convert(stg_dir)
                stg_dir = os.path.dirname(stg_dir)
                stg_dir = os.path.normpath(stg_dir)
                # print(f'DBG src_path:{src_path} src_file:{src_file} stg_dir:{stg_dir}')

                cpip_pkg['src'].append(src_path)
                svc.utils_fs.safe_create_dir(stg_dir)
                svc.utils_fs.safe_copy_file(curr_file, stg_dir, src_file)

                path = os.path.join(stg_dir, src_file)
                svc.log.line(f'{svc.gbl.tag}: {pkg}: staged {path}')
            return

        # missing one of them
        svc.log.warn(f'{svc.gbl.tag}: {pkg}: both "src" and "dst" are needed')

    # --------------------
    ## load the local tools/cpip_publish.json file (for creator projects),
    # aborts if it doesn't exist.
    #
    # @return the packages json content
    def _get_cpip_publish_json(self):
        path = os.path.join('tools', 'cpip_publish.json')
        if not os.path.isfile(path):
            svc.abort(f'{svc.gbl.tag}: cpip_publish.json does not exist: {path}')

        with open(path, 'r', encoding='utf-8') as fp:
            cpip = json.load(fp)
            return cpip

    # --------------------
    ## push staging dir content to local CPIP directory
    #
    # @return None
    def _publish_to_local(self):
        svc.log.highlight(f'{svc.gbl.tag}: pushing to local {svc.cfg.cpip.root_dir} ...')

        # at this point, staging exists, cpip_root_dir exists

        src = self._staging_dir
        dst = self._cpip_root_dir
        dst = svc.utils_fs.full_convert(dst)

        # use rsync to transfer
        # -r recursive
        # -v verbose
        # -c use a different checksum to trigger a push (not mod-time or size change)
        # -h use human-readable numbers
        # -i output a change-summary instead of continuous output
        cmd = f'rsync -rvchi  {src}/ {dst}/'
        svc.log.line(f'push_local: {cmd}')
        svc.utils_ps.run_process(cmd, use_raw_log=False)

    # === clone/pull functions: copy from remote server

    # --------------------
    ## copy all files from remote to local cpip directory
    #
    # @return None
    def _pull_remote_to_local(self):
        svc.log.highlight(f'{svc.gbl.tag}: pulling from server to local {svc.cfg.cpip.root_dir} ...')

        svc.log.line(f'{svc.gbl.tag}: pulling from: {svc.cfg.cpip.server_root} to '
                     f'{self._cpip_root_dir} for platform: {OsSpecific.os_name}')

        # uncomment to debug
        # print(f'@@@ {svc.cfg.cpip.packages} {type(svc.cfg.cpip.packages)}')

        cpip_json = self._get_cpip_json()
        # go through all entries in cpip.packages and install them if for this OS
        for pkg in svc.cfg.cpip.packages:
            if pkg not in cpip_json:
                svc.log.err(f'{svc.gbl.tag}: package in xplat.cpip.packages not found in cpip.json: {pkg}')
                continue

            pkg_data = cpip_json[pkg]

            if pkg_data['deleted']:
                svc.log.warn(f'{svc.gbl.tag}: package is deleted: {pkg}, ignoring...')
                continue

            if OsSpecific.os_name not in pkg_data['platforms'] and pkg_data['platforms'] != ['all']:
                valid_os = ','.join(pkg_data['platforms'])
                svc.log.line(f'{svc.gbl.tag}: package not valid on platform: "{pkg}", valid:{valid_os}')
                continue

            svc.log.line(f'{svc.gbl.tag}: pkg: {pkg} pulling...')
            for src in pkg_data['src']:
                # file is part of url, retain slash
                file = f'{pkg_data["dst"]}/{src}'
                file = file.replace('\\', '/')
                svc.log.line(f'   > {file}')
                self._download_file(file)

    # === get functions; used in pyalamake

    # --------------------
    ## get a CPIP package
    #
    # @param pkg  the package to retrieve
    # @return if found the package info, otherwise None
    def get(self, pkg):
        svc.gbl.rc = 0

        cpip = self._get_cpip_json()

        if pkg not in cpip:
            svc.log.err(f'{svc.gbl.tag}: unknown pkg: {pkg}')
            svc.gbl.rc += 1
            return None

        @dataclass
        class PackageInfo:
            include_dir = self._cpip_root_dir
            src = []

        for file in cpip[pkg]['src']:
            dst_dir = cpip[pkg]['dst']
            if cpip[pkg]['dst'] == '.':
                path = self._convert(os.path.join(self._cpip_root_dir, file))
            else:
                path = self._convert(os.path.join(self._cpip_root_dir, dst_dir, file))
            PackageInfo.src.append(path)

        return PackageInfo

    # === gen functions: used in ut and build (via cmake)

    # --------------------
    ## gen Findcpip.cmake file
    #
    # @return None
    def gen(self):
        svc.gbl.rc = 0

        # check each package in xplat.cfg against the cpip content
        cpip_json = self._get_cpip_json()

        path = os.path.join('Findcpip.cmake')
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            # gen cmake variables for directories
            fp.write(f'set(CPIP_ROOT_DIR {self._cpip_root_dir})\n')
            fp.write(f'set(CPIP_INCLUDE_DIR {self._cpip_root_dir})\n')
            # add additional directories here...
            fp.write('\n')

            # have cmake print them out
            fp.write('message(STATUS "home dir        : ${HOME_DIR}")\n')
            fp.write('message(STATUS "cpip root dir   : ${CPIP_ROOT_DIR}")\n')
            fp.write('message(STATUS "cpip include dir: ${CPIP_INCLUDE_DIR}")\n')
            fp.write('\n')

            self._gen_package_info(fp, cpip_json)

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: rc={svc.gbl.rc}')
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## generate package info in cmake format.
    #
    # @param fp    the file pointer for the output file
    # @param cpip  the contents of the cpip.json file
    # @return None
    def _gen_package_info(self, fp, cpip):
        # generate the source list for all packages
        good_pkgs = 0
        for pkg in svc.cfg.cpip.packages:
            if pkg not in cpip:
                svc.log.warn(f'{svc.gbl.tag}: gen() unknown pkg: {pkg}, skipping')
                svc.gbl.rc += 1
                continue

            if cpip[pkg]['deleted']:
                svc.log.warn(f'{svc.gbl.tag}: gen() cannot use deleted pkg: {pkg}, skipping')
                svc.gbl.rc += 1
                continue

            svc.log.line(f'{svc.gbl.tag}: gen() found pkg: {pkg}')
            good_pkgs += 1
            fp.write('set(CPIP_SRC\n')
            for file in cpip[pkg]['src']:
                dst_dir = cpip[pkg]['dst']
                if cpip[pkg]['dst'] == '.':
                    path = self._convert(file)
                else:
                    path = self._convert(f'{dst_dir}{os.sep}{file}')
                fp.write(f'        ${{CPIP_INCLUDE_DIR}}{os.sep}{path}\n')
            fp.write(')\n')

        if good_pkgs == 0:
            svc.log.warn(f'{svc.gbl.tag}: gen() no valid pkgs found')
            svc.gbl.rc += 1
        else:
            svc.log.line(f'{svc.gbl.tag}: gen() found {good_pkgs} valid pkgs')

    # === common functions

    # --------------------
    ## download file from the server
    #
    # @param file   the file to download
    # @return None
    def _download_file(self, file):
        # url, not a path
        url = f'{svc.cfg.cpip.server_root}/{file}'
        local_path = os.path.join(self._cpip_root_dir, file)

        # ensure dst directory exists
        file_dir = os.path.dirname(local_path)
        svc.utils_fs.safe_create_dir(file_dir)

        try:
            with requests.get(url, stream=True, verify=False, timeout=5) as rsp:
                rsp.raise_for_status()
                with open(local_path, 'wb') as fp:
                    shutil.copyfileobj(rsp.raw, fp)
        except requests.exceptions.HTTPError as excp:
            svc.log.err(excp)

    # --------------------
    ## all of the directories and files needed exist.
    # aborts if cpip.json is missing.
    #
    # @return None
    def _check_cpip_info_exists(self):
        # if path to root_dir and cpip exists
        path = os.path.join(self._cpip_root_dir, 'cpip')
        svc.utils_fs.safe_create_dir(path)

        if not os.path.isfile(self._cpip_json):
            self._download_file('cpip.json')

        if not os.path.isfile(self._cpip_json):
            svc.abort(f'{svc.gbl.tag}: cpip.json does not exist: {self._cpip_json}')

    # --------------------
    ## load the local cpip.json file
    #
    # @return the cpip json content
    def _get_cpip_json(self):
        with open(self._cpip_json, 'r', encoding='utf-8') as fp:
            cpip = json.load(fp)
            return cpip

    # --------------------
    ## convert slashes as appropriate for platform
    #
    # @param path  the path to convert
    # @return the transformed path
    def _convert(self, path):
        if OsSpecific.os_name == 'win':
            return path.replace('/', '\\')
        return path.replace('\\', '/')

    # === ut only

    # --------------------
    ## UT only
    # @return None
    def ut_get_cpip_json(self):
        return self._get_cpip_json()

    # --------------------
    ## UT only
    # @return None
    def ut_get_staged_cpip_json(self):
        path = os.path.join(self._staging_dir, 'cpip.json')
        with open(path, 'r', encoding='utf-8') as fp:
            return json.load(fp)
