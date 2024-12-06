import configparser
import glob
import os
import platform
import re
import sys
from dataclasses import dataclass

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## perform the do_check operation.
# checks all installation and environment
# Do not use any non-built in modules
# Do not use out/ directory
class DoCheck:
    ## list of tools needed; max 3 nodes of the version string
    # if cmd is None, then a specific function must be used
    valid_versions = {
        'python': {
            'techs': ['python', 'cpp', 'arduino'],
            'cmd': None,
            'valid': {
                'ubuntu': ['3.8', '3.9', '3.10'],
                'macos': ['3.9', '3.10'],
                'win': ['3.10'],
                'rpi': [],
            },
            'verbose': True,
        },
        'tkinter': {
            'techs': ['python'],
            'cmd': None,
            'valid': {
                'ubuntu': ['8.6'],
                'macos': ['8.6'],
                'win': ['8.6'],
                'rpi': [],
            },
            'verbose': True,
        },
        'doxygen': {
            'techs': ['python', 'cpp', 'arduino'],
            'cmd': 'doxygen -v',
            'valid': {
                'ubuntu': ['1.8.17', '1.9.1', '1.9.5', '1.10.0'],
                'macos': ['1.9.8', '1.10.0'],
                'win': ['1.10.0', '1.12.0'],
                'rpi': [],
            },
            'verbose': False,
        },
        'libreoffice': {
            'techs': ['python'],
            'cmd': 'libreoffice --version',
            'macos:cmd': 'soffice --version',
            'win:cmd': '"C:\\Program Files\\LibreOffice\\program\\soffice.com" --version',
            'valid': {
                'ubuntu': ['24.2.5', '24.2.6', '24.8.2'],
                'macos': ['7.6.4', '24.2.0', '24.8.2'],
                'win': ['24.2.0'],
                'rpi': [],
            },
            'verbose': False,
        },
        'graphviz': {
            'techs': ['python'],
            'cmd': 'dot -V',
            'valid': {
                'ubuntu': ['2.43.0'],
                'macos': ['9.0.0', '12.1.2'],
                'win': ['9.0.0', '10.0.1', '12.1.2'],
                'rpi': [],
            },
            'verbose': False,
        },
        # deprecated: cmake not used
        # 'cmake': {
        #     'techs': ['cpp', 'arduino'],
        #     'cmd': 'cmake --version',
        #     'valid': {
        #         'ubuntu': ['3.16.3', '3.22.1', '3.25.1'],
        #         'macos': ['3.30.5'],
        #         'win': [],
        #         'rpi': [],
        #     },
        #     'verbose': False,
        # },
        # deprecated: ninja not used
        # 'ninja': {
        #     'techs': ['cpp', 'arduino'],
        #     'cmd': 'ninja --version',
        #     'valid': {
        #         'ubuntu': ['1.10.0', '1.10.1'],
        #         'macos': ['1.12.1'],
        #         'win': [],
        #         'rpi': [],
        #     },
        #     'verbose': False,
        # },
        'gcc': {
            'techs': ['cpp'],
            'cmd': 'gcc --version',
            'valid': {
                'ubuntu': ['9.4.0', '11.4.0', '13.2.0'],
                'macos': ['15.0.0'],
                'win': ['14.2.0'],
                'rpi': [],
            },
            'verbose': False,
        },
        'clang-tidy': {
            'techs': ['cpp', 'arduino'],
            'cmd': 'clang-tidy --version',
            'valid': {
                'ubuntu': ['10.0.0', '14.0.0', '18.1.3'],
                'macos': ['19.1.1'],
                'win': ['18.1.8'],
                'rpi': [],
            },
            'verbose': False,
        },
        'gcovr': {
            'techs': ['cpp', 'arduino'],
            'cmd': 'gcovr --version',
            'valid': {
                'ubuntu': ['4.2', '5.0', '7.2', '7.0', '8.2'],
                'macos': ['8.2'],
                'win': ['8.2'],
                'rpi': [],
            },
            'verbose': False,
        },
        'avr-gcc': {
            'techs': ['arduino'],
            'cmd': 'avr-gcc --version',
            'valid': {
                'ubuntu': ['5.4.0', '7.3.0'],
                'macos': [],
                'win': ['14.2.0'],
                'rpi': [],
            },
            'verbose': False,
        },
        'avrdude': {
            'techs': ['arduino'],
            'cmd': 'avrdude -?',
            'valid': {
                'ubuntu': ['6.3', '7.1'],
                'macos': [],
                'win': ['6.3'],
                'rpi': [],
            },
            'verbose': False,
        },
        'avr-gdb': {
            'techs': ['arduino'],
            'cmd': 'avr-gdb --version',
            'win:cmd': 'echo "0.0"',  # doesn't install in windows
            'valid': {
                'ubuntu': ['8.1.0', '10.1.90', '15.0.50'],
                'macos': [],
                'win': ['0.0'],
                'rpi': [],
            },
            'verbose': False,
        },
        'ruby': {
            'techs': ['cpp'],
            'cmd': 'ruby --version',
            'valid': {
                'ubuntu': ['3.0.2', '3.2.3'],
                'macos': ['3.3.5'],
                'win': ['3.3.6'],
                'rpi': [],
            },
            'verbose': False,
        },
        'swig': {
            'techs': ['cpp'],
            'cmd': 'swig --version',
            'win:cmd': 'swig -version',
            'valid': {
                'ubuntu': ['4.3.0'],
                'macos': ['4.2.1'],
                'win': ['4.2.1'],
                'rpi': [],
            },
            'verbose': False,
        }
    }

    # --------------------
    ## constructor
    def __init__(self):
        ## holds additional scripts to check for permissions
        self._scripts = []

    # --------------------
    ## do_check mainline.
    #
    # @return None
    def run(self):
        svc.log.highlight(f'{svc.gbl.tag}: starting...')

        self._check_ostype()
        # python is needed by arduino and cpp projects as well
        self._check_python_version()

        # make sure mod names are correct first
        self._check_mod_names()

        # TODO delete if not needed
        # ensure version.json and build_info are created
        # if svc.gbl.rc == 0 and dogen == 'dogen':
        #     # only if modnames are ok
        #     svc.gen_files.all(dogen=dogen)

        self._gen_license()

        # check everything else
        self._check_versions()
        self._check_bash_scripts()
        self._check_common()

        if svc.cfg.mod_tech == 'python':
            self._check_publish_files()
            self._check_pypi()
            self._check_tkinter()

        if svc.cfg.mod_tech == 'arduino':
            self._check_arduino()

        svc.gbl.rc = svc.gbl.rc
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## check the OS name and platform are recognized
    #
    # @return None
    def _check_ostype(self):
        svc.log.line(f'os_name : {os.name}:{OsSpecific.os_name}')

        svc.log.line(f'system  : {platform.system()}')
        # Linux: Linux
        # Mac: Darwin
        # Windows: Windows
        # RPI: ??

        svc.log.line(f'platform: {sys.platform}')
        # Linux: linux (lower case)
        # Mac: ??
        # Win MSYS2: msys (need to confirm)
        # Win MING : mingw64
        # WIN WSL  : linux2
        # RPI: ??

    # --------------------
    ## check the python version
    #
    # @return True if a valid version, False otherwise
    def _check_python_version(self):
        svc.log.highlight('python version:')
        version = sys.version.replace('\n', ' ')
        svc.log.line(f'version : {version}')
        svc.log.line(f'info    : {sys.version_info}')

        version = f'{sys.version_info.major}.{sys.version_info.minor}'
        self._check_tool_version2('python', version, True)

    # --------------------
    ## check all tool versions
    #
    # @return None
    def _check_versions(self):
        msgs = []
        ok = True
        for tool, item in self.valid_versions.items():
            if svc.cfg.mod_tech not in item['techs']:
                # uncomment to debug
                # svc.log.dbg(f'check_versions: tech:{svc.cfg.mod_tech} skipping {tool}')
                continue

            # check if there is an os_specific cmd to run
            os_cmd = f'{OsSpecific.os_name}:cmd'
            if os_cmd in item and item[os_cmd] is not None:
                ok = ok and self._check_tool_version(msgs, tool, item, item[os_cmd])
                continue

            # no os_specific one, use the generic one
            if item['cmd'] is not None:
                ok = ok and self._check_tool_version(msgs, tool, item, item['cmd'])
                continue

        if ok:
            svc.log.ok('all tool versions')
        else:
            for msg in msgs:
                svc.gbl.rc += 1
                svc.log.err(msg)

    # --------------------
    ## check the version for the given tool
    #
    # @param msgs    list of error messages to display
    # @param key     the name of the tool
    # @param item    tool information from valid_versions
    # @param cmd     the command to use
    # @return None
    def _check_tool_version(self, msgs, key, item, cmd):
        rc, out = svc.utils_ps.run_cmd(cmd)
        ok = True
        if rc != 0:
            ok = False
            msgs.append(f'{key} version failed, rc:{rc}, out:"{out}"')
        else:
            # note: 3rd spot is optional
            m = re.search(r'(\d+\.\d+(\.\d+)?)', out)
            if m:
                version = m.group(1)
            else:
                version = out
            self._check_tool_version2(key, version, item['verbose'])

        return ok

    # --------------------
    ## checks version on the given tool
    #
    # @param tool_name    the tool to check
    # @param act_version  the actual version of the tool
    # @param verbose      flag to indicate whether to log passing chacks or not
    # @return None
    def _check_tool_version2(self, tool_name, act_version, verbose):
        valid = self.valid_versions[tool_name]['valid'][OsSpecific.os_name]
        # version is sometimes a float
        if str(act_version) in valid:
            if verbose:
                svc.log.ok(f'{tool_name} {act_version}')
        else:
            svc.gbl.rc += 1
            svc.log.err(f'{tool_name} valid versions {valid}, actual: {act_version}')

    # --------------------
    ## check for the existence of $HOME/.pypirc and its content
    #
    # @return None
    def _check_pypi(self):
        home = os.path.expanduser('~')
        path = os.path.join(home, '.pypirc')
        exists = os.path.isfile(path)
        msg = f'{".pypirc exists": <15}: {exists}'
        svc.log.check(exists, msg)

        if exists:
            self._check_pypi_content(path)
        else:
            svc.gbl.rc += 1

    # --------------------
    ## check for the existence of $HOME/.pypirc and its content
    #
    # @return None
    def _check_tkinter(self):
        # >>> import tkinter
        # >>> tkinter.TkVersion
        # 8.6
        import importlib.util
        tkmod = importlib.util.find_spec('tkinter')
        if tkmod is None:
            svc.log.warn('tkinter not installed')
        else:
            import tkinter
            version = tkinter.TkVersion
            self._check_tool_version2('tkinter', version, True)

    # --------------------
    ## check the content of the .pypirc file
    #
    # @param path the path to the file
    # @return None
    def _check_pypi_content(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        msg = ''
        ok = 'pypi' in config.sections()
        if not ok:
            svc.gbl.rc += 1
            msg += 'missing "pypi" section'
            svc.log.err(msg)
            return

        msgs = []
        # check username
        if 'username' not in config['pypi']:
            msgs.append('missing pypi.username')
            ok = False
        elif config['pypi']['username'] != '__token__':
            msgs.append('pypi.username should be "__token__"')
            ok = False

        # check password
        if 'password' not in config['pypi']:
            msgs.append('missing pypi.password')
            ok = False

        svc.log.check_all(ok, f'{".pypirc content": <15}', msgs)

    # --------------------
    ## check permissions on the executable scripts
    #  * all scripts that start with do_*
    #  * any given in self._scripts
    #
    # @return None
    def _check_bash_scripts(self):
        scripts = glob.glob('do*')
        self._scripts.extend(scripts)
        ok = True
        for path in self._scripts:
            if not os.path.isfile(path):
                continue
            ok = ok and self._check_script(path)
        if ok:
            svc.log.ok('execute permissions')

    # --------------------
    ## checks the permissions for the given script
    #
    # @param path   the script to check
    # @return None
    def _check_script(self, path):
        ok = os.access(path, os.X_OK)
        if not ok:
            svc.gbl.rc += 1
            msg = f'execute permission missing: {path}'
            svc.log.err(msg)
        return ok

    # --------------------
    ## check values against xplat.cfg content
    #
    # @return None
    def _check_common(self):
        self._check_doxyfile()
        self._check_gitignore()
        self._check_gitconfig()
        self._check_license()
        self._check_requirements_txt()
        self._check_home()

    # --------------------
    ## check module names
    #
    # @return None
    def _check_mod_names(self):
        # check for default mod_names
        if svc.cfg.is_module:
            svc.log.highlight(f'{svc.cfg.mod_name} is a module')
        else:
            svc.log.highlight(f'{svc.cfg.mod_name} is not a module')

        if svc.cfg.mod_name == 'module-name':
            svc.gbl.rc += 1
            svc.log.err(f'{svc.cfg.mod_name} must be changed to correct name')
        if svc.cfg.mod_dir_name == 'module_name':
            svc.gbl.rc += 1
            svc.log.err(f'{svc.cfg.mod_dir_name} must be changed to correct dir name')

        # check mod names are correct format
        if not svc.cfg.mod_name:
            svc.gbl.rc += 1
            svc.log.err('mod_name in xplat.cfg not set')
        elif '_' in svc.cfg.mod_name:
            svc.gbl.rc += 1
            svc.log.err(f'mod_name should contain "-", not "_": {svc.cfg.mod_name}')
        else:
            svc.log.ok(f'{"mod_name": <18}: {svc.cfg.mod_name}')

        if svc.cfg.mod_dir_name == '':
            svc.gbl.rc += 1
            svc.log.err('mod_dir_name in xplat.cfg not set')
        elif '-' in svc.cfg.mod_dir_name:
            svc.gbl.rc += 1
            svc.log.err(f'mod_dir_name should contain "_", not "-": {svc.cfg.mod_dir_name}')
        else:
            svc.log.ok(f'{"mod_dir_name": <18}: {svc.cfg.mod_dir_name}')

    # --------------------
    ## check Doxyfile
    #
    # @return None
    def _check_doxyfile(self):
        tag = 'Doxyfile'
        fname = os.path.join(svc.utils_fs.root_dir, 'Doxyfile')
        if not os.path.isfile(fname):
            svc.log.warn(f'{tag}: Doxyfile not found, skipping check')
            return

        @dataclass
        class state:  # pylint: disable=invalid-name
            found_version = False
            found_name = False
            found_exclude = False
            ok = True

        with open(fname, 'r', encoding='UTF-8') as fp:
            for line in fp:
                line = line.strip()

                self._doxyfile_project_name(tag, line, state)
                self._doxyfile_project_number(tag, line, state)
                self._doxyfile_excludes(tag, line, state)

        if not state.found_version:
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: "PROJECT_NUMBER" line not found')
            state.ok = False

        if not state.found_name:
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: "PROJECT_NAME" line not found')
            state.ok = False

        if not state.found_exclude:
            # even if the module doesn't use build_info, Doxyfile can exclude it
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: "EXCLUDE" build_info line not found')
            state.ok = False

        if state.ok:
            svc.log.ok(f'{tag}')

    # --------------------
    ## check Doxyfile project name
    # e.g. PROJECT_NAME = "gui-api-tkinter Module" or
    # for apps: PROJECT_NAME = "gui-api-tkinter App"
    #
    # @param tag    the logging tag
    # @param line   the doxyfile line to check
    # @param state  (dict) holds the current state of the checks
    # @return None
    def _doxyfile_project_name(self, tag, line, state):
        m = re.search(r'PROJECT_NAME\s*=\s*(".+")$', line)
        if not m:
            return

        # found it
        if svc.cfg.is_module:
            exp_name = 'Module'
        else:
            exp_name = 'App'

        state.found_name = True
        if m.group(1) != f'"{svc.cfg.mod_name} {exp_name}"':
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: "PROJECT_NAME" line does not match "{svc.cfg.mod_name} {exp_name}", '
                        f'actual: {line}')
            state.ok = False

    # --------------------
    ## check Doxyfile project version
    # e.g. PROJECT_NUMBER = 0.0.1
    #
    # @param tag    the logging tag
    # @param line   the doxyfile line to check
    # @param state  (dict) holds the current state of the checks
    # @return None
    def _doxyfile_project_number(self, tag, line, state):
        m = re.search(r'PROJECT_NUMBER\s*=\s*(.+)\s*$', line)
        if not m:
            return

        # found it
        state.found_version = True
        if m.group(1) != f'v{svc.cfg.version}':
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: "PROJECT_NUMBER" version does not match version.json: {svc.cfg.version}, '
                        f'actual: {line}')
            state.ok = False

    # --------------------
    ## check Doxyfile excludes
    # e.g. EXCLUDE += ./.../lib/build_info.py or
    # for apps EXCLUDE += ./lib/build_info.py
    #
    # @param tag    the logging tag
    # @param line   the doxyfile line to check
    # @param state  (dict) holds the current state of the checks
    # @return None
    def _doxyfile_excludes(self, tag, line, state):
        if OsSpecific.os_name == 'win':
            slash = '\\\\'
        else:
            slash = '/'
        if svc.cfg.mod_tech == 'python':
            m = re.search(fr'EXCLUDE\s*\+=\s*(.+){slash}build_info\.py', line)
        else:
            m = re.search(fr'EXCLUDE\s*\+=\s*(.+){slash}build_info\.txt', line)
        if not m:
            return

        if svc.cfg.is_module:
            if svc.cfg.mod_tech == 'python':
                exp_dir = f'.{os.sep}{svc.cfg.mod_dir_name}{os.sep}lib'
            else:
                exp_dir = f'.{os.sep}lib'
        else:
            if svc.cfg.mod_tech == 'python':
                exp_dir = f'.{os.sep}lib'
            else:
                exp_dir = f'.{os.sep}src'

        # found it
        state.found_exclude = True
        if m.group(1) != exp_dir:
            svc.gbl.rc += 1
            if svc.cfg.mod_tech == 'python':
                svc.log.err(f'{tag}: "EXCLUDE" build_info line does not match {exp_dir}/build_info.py, '
                            f'actual: {line}')
            else:
                svc.log.err(f'{tag}: "EXCLUDE" build_info line does not match {exp_dir}/build_info.txt, '
                            f'actual: {line}')
            state.ok = False

    # --------------------
    ## check .gitignore file
    #
    # @return None
    def _check_gitignore(self):
        tag = '.gitignore'

        fname = self._get_gitignore_path()
        if fname is None:
            return

        if not os.path.isfile(fname):
            svc.log.err(f'{tag}: file not found: {fname}')
            return

        @dataclass
        class state:  # pylint: disable=invalid-name
            found_buildinfo = False
            ok = True

        with open(fname, 'r', encoding='UTF-8') as fp:
            for line in fp:
                line = line.strip()

                if svc.cfg.mod_tech in ['cpp', 'arduino']:
                    if re.search(r'^\s*/build_info.txt\s*$', line):
                        state.found_buildinfo = True
                        continue
                else:  # python
                    if re.search(r'^\s*/build_info.py\s*$', line):
                        state.found_buildinfo = True
                        continue

        if not state.found_buildinfo:
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: build_info line not found')
            state.ok = False

        if state.ok:
            svc.log.ok(f'{tag}')

    # --------------------
    ## get the path to the local gitignore file
    #
    # @return path to gitignore
    def _get_gitignore_path(self):
        if svc.cfg.mod_tech == 'cpp':
            if svc.cfg.is_module:
                path = os.path.join(svc.utils_fs.root_dir, 'lib', '.gitignore')
            else:
                path = os.path.join(svc.utils_fs.root_dir, 'src', '.gitignore')
        elif svc.cfg.mod_tech == 'arduino':
            path = os.path.join(svc.utils_fs.root_dir, 'src', '.gitignore')
        else:  # python
            if svc.cfg.is_module:
                mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
                if not os.path.isdir(mod_dir):
                    svc.log.warn(f'check_gitignore: dir does not exist: {mod_dir}')
                    svc.gbl.rc = 1
                    return None

                path = os.path.join(str(mod_dir), 'lib', '.gitignore')
            else:
                path = os.path.join(svc.utils_fs.root_dir, 'lib', '.gitignore')

        return path

    # --------------------
    ## check .gitignore file
    #
    # @return None
    def _check_gitconfig(self):
        tag = '.gitconfig'
        path = os.path.join(os.path.expanduser('~'), '.gitconfig')

        ok = True
        if not os.path.isfile(path):
            svc.gbl.rc += 1
            svc.log.err(f'{tag} cannot find {path}')
            return

        config = configparser.ConfigParser()
        config.read(path)
        ok = ok and self._check_gitconfig_section(tag, config, 'pull', 'rebase', 'false')
        ok = ok and self._check_gitconfig_section(tag, config, 'push', 'autoSetupRemote', 'true')

        if ok:
            svc.log.ok(f'{tag}')

    # --------------------
    ## check a section in the .gitignore file
    #
    # @param tag      the logging tag
    # @param config   reference to the configparser
    # @param section  the section name
    # @param name     the name of the line
    # @param value    the value of the line
    # @return return True if everything is okay in the section, false otherwise
    def _check_gitconfig_section(self, tag, config, section, name, value):
        ok = True
        if section not in config.sections():
            svc.gbl.rc += 1
            ok = False
            svc.log.err(f'{tag} cannot find "{section}" section')
        elif name not in config[section]:
            svc.gbl.rc += 1
            ok = False
            svc.log.err(f'{tag} cannot find "{name}" in "{section}" section')
        elif config[section][name] != value:
            svc.gbl.rc += 1
            ok = False
            svc.log.err(f'{tag} {section}.{name} should be "{value}", actual: {config[section][name]}')
        return ok

    # --------------------
    ## check license file
    #
    # @return None
    def _check_license(self):
        # * check license, for "Copyright line"
        tag = 'LICENSE.txt'
        fname = 'LICENSE.txt'
        path = os.path.join(svc.utils_fs.root_dir, fname)

        if svc.cfg.is_module and not os.path.isfile(path):
            svc.gbl.rc += 1
            svc.log.err(f'{tag} modules must have a LICENSE.txt file')
            return

        if not svc.cfg.is_module and not os.path.isfile(path):
            # apps may or may not have a LICENSE.txt file
            return

        with open(path, 'r', encoding='UTF-8') as fp:
            line1 = fp.readline().strip()
            line2 = fp.readline().strip()
            line3 = fp.readline().strip()
            line4 = fp.readline().strip()
            line5 = fp.readline().strip()
            line6 = fp.readline().strip()

            ok = True
            # MIT License
            if line1 != f'{svc.cfg.license} License':
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line1 invalid license line: "{line1}"')

            if line2:
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line2 should be blank: "{line2}"')

            # Copyright (c) since (etc.)
            m = re.search(r'^Copyright \(c\) since \d{4}: ', line3)
            if not m:
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line3 invalid copyright line: "{line3}"')

            # a one-line description
            m = re.search(r'^description: ', line4)
            if not m:
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line4 should contain a description: "{line4}"')

            m = re.search(r'^author: .* email: .*$', line5)
            if not m:
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line5 should have author and email: "{line5}"')

            if line6:
                svc.gbl.rc += 1
                ok = False
                svc.log.err(f'{fname}: line6 should be blank: "{line6}"')

            if ok:
                svc.log.ok(f'{fname}')

    # --------------------
    ## check files used in module publish.
    # * if module, must exist
    # * if app, must not exist
    #
    # @return None
    def _check_publish_files(self):
        tag = 'publish'
        for fname in ['do_publish']:
            path = os.path.join(svc.utils_fs.root_dir, fname)
            if svc.cfg.is_module and not os.path.isfile(path):
                svc.gbl.rc += 1
                svc.log.err(f'{tag}" modules must have a "{fname}" file')
            elif not svc.cfg.is_module and os.path.isfile(path):
                svc.gbl.rc += 1
                svc.log.err(f'{tag}: apps should not have a "{fname}" file')

    # --------------------
    ## check requirements file
    #
    # @return None
    def _check_requirements_txt(self):
        ok = True
        tag = 'requirements.txt'
        path = os.path.join(svc.utils_fs.root_dir, 'tools', 'requirements.txt')

        if not os.path.isfile(path):
            svc.gbl.rc += 1
            svc.log.err(f'{tag} does not exist: {path}')
            return

        if ok:
            svc.log.ok(f'{tag}')

    # --------------------
    ## check definition of HOME
    #
    # @return None
    def _check_home(self):
        py_home = os.path.expanduser('~')
        if OsSpecific.os_name == 'win':
            py_home2 = py_home.replace('\\', '/')
            py_home2 = py_home2.replace('C:', '/c')
            _, bash_home = svc.utils_ps.run_cmd('echo ~', msys2=True)
        else:
            py_home2 = py_home
            _, bash_home = svc.utils_ps.run_cmd('echo ~')

        if py_home2 == bash_home:
            svc.log.ok(f'home directory: {bash_home}')
        else:
            svc.log.warn('home directory (~) and pyhon home are defined differently:')
            svc.log.warn(f'   python: {py_home}')
            svc.log.warn(f'   bash  : {bash_home}')

    # --------------------
    ## check arduino libraries etc.
    #
    # @return None
    def _check_arduino(self):
        tag = 'arduino'

        if OsSpecific.os_name == 'macos':
            path = os.path.expanduser('~/Library/Arduino15')
        elif OsSpecific.os_name == 'win':
            path = os.path.expanduser('~/AppData/Local/Arduino15')
        else:
            path = os.path.join(os.sep, 'usr', 'share', 'arduino')
        if not os.path.isdir(path):
            svc.gbl.rc += 1
            svc.log.err(f'{tag}: missing {path}, run "sudo apt install arduino"')
        elif OsSpecific.os_name == 'ubuntu':
            # /usr/share/arduino/lib/version.txt
            version = os.path.join(path, 'lib', 'version.txt')
            with open(version, 'r', encoding='utf-8') as fp:
                line = fp.readline()
                svc.log.ok(f'{tag}: found lib version: {line.strip()}')

        if OsSpecific.os_name == 'ubuntu':
            path = os.path.join(os.sep, 'usr', 'lib', 'gcc', 'avr')
            if not os.path.isdir(path):
                svc.gbl.rc += 1
                svc.log.err(f'{tag}: missing {path}, run "sudo apt install avr-libc"')
            else:
                dirs = os.listdir(path)
                for subdir in dirs:
                    svc.log.ok(f'{tag}: found avr lib version: {subdir}')

    # --------------------
    ## gen licence file using template
    #
    # @return None
    def _gen_license(self):  # pylint: disable=too-many-branches
        svc.utils_fs.safe_delete_file('LICENSE.txt')

        # generate the LICENSE.txt file
        src = os.path.join(svc.utils_fs.root_dir, 'tools', 'xplat_utils', 'license_template.txt')
        dst = os.path.join(svc.utils_fs.root_dir, 'LICENSE.txt')
        with open(dst, 'w', encoding='utf-8', newline='\n') as fp_dst:
            with open(src, 'r', encoding='utf-8') as fp_src:
                for line in fp_src:
                    while True:
                        m = re.search(r'\$\$([^$]+)\$\$', line)
                        if not m:
                            # uncomment to debug
                            # log.dbg(f'line: {line.strip()}')
                            fp_dst.write(line)
                            break

                        vrbl = m.group(1)
                        if vrbl == 'module-name':
                            val = getattr(svc.cfg, 'mod_name')
                        elif vrbl == 'lic-tech':
                            if svc.cfg.mod_tech == 'python':
                                val = 'Python'
                            elif svc.cfg.mod_tech == 'cpp':
                                val = 'C/C++'
                            elif svc.cfg.mod_tech == 'arduino':
                                val = 'Arduino'
                            else:
                                svc.log.warn(f'gen_license: unknown mod_tech found: {svc.cfg.mod_tech}')
                                val = svc.cfg.mod_tech
                        elif vrbl == 'lic-proj-type':
                            if svc.cfg.is_module:
                                if svc.cfg.mod_tech == 'python':
                                    val = 'Module'
                                else:
                                    val = 'Library'
                            else:
                                val = 'App'
                        elif vrbl == 'lic-year':
                            val = getattr(svc.cfg, 'lic_year', None)
                            if val is None:
                                val = '2024'
                                svc.log.warn(f'gen_license: unknown lic_year, using {val}')
                        elif vrbl == 'lic-desc':
                            val = getattr(svc.cfg, 'lic_desc', None)
                            if val is None:
                                val = svc.cfg.do_doc.doxy_desc
                        else:
                            val = getattr(svc.cfg, vrbl)
                        # uncomment to debug
                        # log.dbg(f'grp:{m.group(1)} line:{line.strip()}')
                        line = line.replace(f'$${vrbl}$$', val)

        svc.gbl.overallrc += svc.gbl.rc
