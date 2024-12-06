import os
import re

from .svc import svc


# --------------------
## Operating System Abstraction Layer; provides functions to make cross-platform behavior similar
class Osal:
    # --------------------
    ## fix paths for cross-platforms
    #
    # @param path   the path to fix
    # @return the fixed path
    @classmethod
    def fix_path(cls, path):
        path = os.path.expanduser(path)
        if svc.gbl.os_name == 'win':
            # assumes there is only one ":" and it is for a drive letter
            m = re.search(r'(.*)(.):(.*)', path)
            if m:
                drive = m.group(2).lower()
                path = f'{m.group(1)}/{drive}/{m.group(3)}'
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        return path

    # --------------------
    ## get the homebrew link libraries root directory
    #
    # @return the homebrew link lib root dir
    @classmethod
    def homebrew_link_dirs(cls):
        return '/opt/homebrew/lib'

    # --------------------
    ## get the homebrew includes root directory
    #
    # @return the homebrew includes dir
    @classmethod
    def homebrew_inc_dirs(cls):
        return '/opt/homebrew/include'

    # --------------------
    ## get the root of the arduino cores, tools, etc.
    #
    # @return the root arduino directory
    @classmethod
    def arduino_root_dir(cls):
        if svc.gbl.os_name == 'macos':
            path = os.path.expanduser('~/Library/Arduino15')
        elif svc.gbl.os_name == 'win':
            path = os.path.expanduser('~/AppData/Local/Arduino15')
        else:
            path = '/usr/share/arduino'
        # do not fix_path()
        return path

    # --------------------
    ## get the library directory for arduino core source files
    #
    # @param arduino_root_dir   the root of the arduino directory system
    # @return the root libdir
    @classmethod
    def arduino_core_libdir(cls, arduino_root_dir):
        if svc.gbl.os_name == 'macos':
            path = f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino'
        elif svc.gbl.os_name == 'win':
            path = f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino'
        else:
            path = f'{arduino_root_dir}/hardware/arduino/avr/cores/arduino'
        # do not fix_path()
        return path

    # --------------------
    ## get the list of included directories for arduino core
    #
    # @param arduino_root_dir   the root of the arduino directory system
    # @return the list of include directories
    @classmethod
    def arduino_core_includes(cls, arduino_root_dir):
        if svc.gbl.os_name == 'macos':
            incs = [
                f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino',
                f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/variants/standard',
            ]
        elif svc.gbl.os_name == 'win':
            incs = [
                f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/cores/arduino',
                f'{arduino_root_dir}/packages/arduino/hardware/avr/1.8.6/variants/standard',
            ]
        else:
            incs = [
                f'{arduino_root_dir}/hardware/arduino/avr/cores/arduino',
                f'{arduino_root_dir}/hardware/arduino/avr/variants/standard',
            ]
        # do not fix_path()
        return incs

    # --------------------
    ## get the directory for avrdude.conf
    #
    # @param arduino_root_dir   the root of the arduino directory system
    # @return the avrdude directory
    @classmethod
    def avrdude_dir(cls, arduino_root_dir):
        if svc.gbl.os_name == 'macos':
            path = '/opt/homebrew/etc'
        elif svc.gbl.os_name == 'win':
            path = f'{arduino_root_dir}/packages/arduino/tools/avrdude/6.3.0-arduino17/etc'
            # TODO /c/Users/micro/AppData/Local/Arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17/etc
        else:
            path = f'{arduino_root_dir}/hardware/tools'
        # do not fix_path()
        return path

    # --------------------
    ## return default gtest include directories
    #
    # @return the list of include directories
    @classmethod
    def gtest_includes(cls):
        incs = []
        if svc.gbl.os_name == 'win':
            incs.append('c:/msys64/mingw64/include')
        # do not fix_path()
        return incs

    # --------------------
    ## return default gtest link directories
    #
    # @return the list of link directories
    @classmethod
    def gtest_link_dirs(cls):
        dirs = []
        if svc.gbl.os_name == 'win':
            dirs.append('c:/msys64/mingw64/lib')
        # do not fix_path()
        return dirs

    # --------------------
    ## return default ruby include directories
    #
    # @return the list of include directories
    @classmethod
    def ruby_includes(cls):
        incs = []
        if svc.gbl.os_name == 'win':
            incs.append('C:/Ruby33-x64/include/ruby-3.3.0')
            incs.append('C:/Ruby33-x64/include/ruby-3.3.0/x64-mingw-ucrt')
        elif svc.gbl.os_name == 'macos':
            incs.append('/opt/homebrew/Cellar/ruby/3.3.5/include/ruby-3.3.0/')
            incs.append('/opt/homebrew/Cellar/ruby/3.3.5/include/ruby-3.3.0/arm64-darwin23')
        else:
            # TODO check with macos
            # ubuntu
            # upgraded to ruby 3.2 in ubuntu 24.04
            incs.append('/usr/include/ruby-3.2.0')
            incs.append('/usr/include/x86_64-linux-gnu/ruby-3.2.0')
            # incs.append('/usr/include/ruby-3.0.0')
            # incs.append('/usr/include/x86_64-linux-gnu/ruby-3.0.0')

        # do not fix_path()
        return incs

    # --------------------
    ## return default ruby link directories
    #
    # @return the list of link directories
    @classmethod
    def ruby_link_dirs(cls):
        dirs = []
        if svc.gbl.os_name == 'win':
            dirs.append('C:/Ruby33-x64/lib')
        elif svc.gbl.os_name == 'macos':
            dirs.append('/opt/homebrew/Cellar/ruby/3.3.5/lib')
        # do not fix_path()
        return dirs

    # --------------------
    ## return default link libraries needed for ruby
    #
    # @return the list of link libraries
    @classmethod
    def ruby_link_libs(cls):
        libs = []
        if svc.gbl.os_name == 'win':
            libs.append('x64-ucrt-ruby330.dll')
        # do not fix_path()
        return libs

    # --------------------
    ## return default python include directories
    #
    # @return the list of include directories
    @classmethod
    def python_includes(cls):
        incs = []
        if svc.gbl.os_name == 'macos':
            incs.append(
                '/opt/homebrew/Cellar/python@3.10/3.10.15/Frameworks/Python.framework/Versions/3.10/include/python3.10')
        elif svc.gbl.os_name == 'ubuntu':
            # upgraded from 3.10 to 3.12 in ubuntu 24.04
            # incs.append('/usr/include/python3.10')
            incs.append('/usr/include/python3.12')
        # do not fix_path()
        return incs

    # --------------------
    ## return default link libraries needed for ruby
    #
    # @return the list of link libraries
    @classmethod
    def python_link_libs(cls):
        libs = []
        if svc.gbl.os_name == 'macos':
            libs.append(
                '/opt/homebrew/Cellar/python@3.10/3.10.15/Frameworks/Python.framework/Versions/3.10/lib/python3.10/config-3.10-darwin')
        # do not fix_path()
        return libs
