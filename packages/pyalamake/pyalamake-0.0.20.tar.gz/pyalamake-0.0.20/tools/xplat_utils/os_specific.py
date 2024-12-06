import getpass
import os
import platform
import subprocess
import sys

from .svc import svc


# -------------------
## runs OS specific commands
# there are four recognized OS:
#  * Ubuntu
#  * Mac
#  * Windows
#  * RPi
class OsSpecific:
    ## holds the OS name
    os_name = 'unknown'
    ## list of valid OS
    os_valid = ['ubuntu', 'macos', 'win', 'rpi']
    ## holds the OS version info
    os_version = 'unknown'
    ## holds the python version
    python_version = 'unknown'

    ## holds a reference to the implemenation class for the current OS
    impl = None

    # -------------------
    ## implements the Windows specific commands
    class Win:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'win'

        # -------------------
        ## holds OS information
        #
        # @return string indicating OS info
        def os_version(self):
            return f'win32 {platform.system()} {platform.release()}'

        # # -------------------
        # ## returns the given command line
        # # Windows implementation needs the un-parsed command line
        # #
        # # @param cmdline the command line to parse
        # # @return the given cmdline
        # def parse_command_line(self, cmdline):
        #     return 'cmd /C ' + cmdline

        # # -------------------
        # ## returns a preexec_fn for Popen calls
        # # not used in Windows implementation
        # #
        # # @return None
        # def preexec_fn(self):
        #     return None

        # # -------------------
        # ## returns the package manager
        # # Windows does not have a package manager
        # #
        # # @return None
        # def package_manager(self):
        #     return None

        # # -------------------
        # ## kill the process group with the given process ID
        # # Windows does not have a process group. TaskKill will delete a tree of processes
        # #
        # # @param pid   the process ID to kill
        # # @return None
        # def kill(self, pid):
        #     # TODO move to utils_ps; may or may not work on Windows
        #     cmd = ['TASKKILL', '/F', '/T', '/PID', str(pid)]
        #     proc = subprocess.Popen(cmd,  # pylint: disable=consider-using-with
        #                             bufsize=0,
        #                             universal_newlines=True,
        #                             stdin=None,
        #                             stdout=subprocess.PIPE,
        #                             stderr=subprocess.STDOUT)
        #     svc.log.output('OsSpecific:kill', proc.stdout.readlines())

        # # -------------------
        # ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        # #
        # # @param arg  the command line argument to parse
        # # @return the parsed command line as required for the platform
        # def split_args(self, arg):
        #     re_cmd_lex = r'''"((?:""|\\["\\]|[^"])*)"?()|(\\\\(?=\\*")|\\")|(&&?|\|\|?|\d?>|[<])|([^\s"&|<>]+)|(\s+)|(.)'''
        #
        #     args = []
        #     accu = None  # collects pieces of one arg
        #     for quotes, qss, esc, pipe, word, white, fail in re.findall(re_cmd_lex, arg):
        #         if word:
        #             pass  # most frequent
        #         elif esc:
        #             word = esc[1]
        #         elif white or pipe:
        #             if accu is not None:
        #                 args.append(accu)
        #             if pipe:
        #                 args.append(pipe)
        #             accu = None
        #             continue
        #         elif fail:
        #             raise ValueError('invalid or incomplete shell string')
        #         elif quotes:
        #             word = quotes.replace('\\"', '"').replace('\\\\', '\\')
        #             word = word.replace('""', '"')
        #         else:
        #             word = qss  # may be even empty; must be last
        #
        #         accu = (accu or '') + word
        #
        #     if accu is not None:
        #         args.append(accu)
        #
        #     return args

    # -------------------
    ## implements the Mac specific commands
    class Mac:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## holds OS information
        #
        # @return string indicating OS info
        def os_version(self):
            return f'macOS {platform.mac_ver()[0]}'

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'macos'

        # # -------------------
        # ## parses the command line into an array of tokens as required by the shell
        # #
        # # @param cmdline the command line to parse
        # # @return an array of elements from the given cmdline
        # def parse_command_line(self, cmdline):
        #     return shlex.split(cmdline)

        # # -------------------
        # ## returns a preexec_fn for Popen calls
        # #
        # # @return the sid required by Popen calls
        # def preexec_fn(self):
        #     return os.setsid

        # # -------------------
        # ## returns the package manager
        # #
        # # @return Brew package manager
        # def package_manager(self):
        #     return 'brew'

        # # -------------------
        # ## kill the process group with the given process ID
        # #
        # # @param pid   the process ID to kill
        # # @return None
        # def kill(self, pid):
        #     os.killpg(os.getpgid(pid), signal.SIGTERM)

        # # -------------------
        # ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        # #
        # # @param arg  the command line argument to parse
        # # @return the parsed command line as required for the platform
        # def split_args(self, arg):
        #     return shlex.split(arg)

    # -------------------
    ## implements the Ubuntu specific commands
    class Ubuntu:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'ubuntu'

        # -------------------
        ## holds OS information
        #
        # @return string indicating OS info
        def os_version(self):
            proc = subprocess.Popen(["lsb_release", "-a"],  # pylint: disable=consider-using-with
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT
                                    )
            (out, _) = proc.communicate()
            out = out.decode('utf-8')

            version = 'notset'
            codename = 'notset'
            for line in out.split('\n'):
                # print(f'line: "{line}"')
                args = line.split('\t')
                if args[0] == 'Release:':
                    version = args[1]
                elif args[0] == 'Codename:':
                    codename = args[1]
            return f'Ubuntu {version} {codename}'

        # # -------------------
        # ## parses the command line into an array of tokens as required by the shell
        # #
        # # @param cmdline the command line to parse
        # # @return an array of elements from the given cmdline
        # def parse_command_line(self, cmdline):
        #     return shlex.split(cmdline)

        # # -------------------
        # ## returns a preexec_fn for Popen calls
        # # not used in Ubuntu implementation
        # #
        # # @return None
        # def preexec_fn(self):
        #     return None

        # # -------------------
        # ## returns the package manager
        # #
        # # @return APT package manager
        # def package_manager(self):
        #     return 'apt'

        # # -------------------
        # ## kill the process group with the given process ID
        # #
        # # @param pid   the process ID to kill
        # # @return None
        # def kill(self, pid):
        #     os.killpg(os.getpgid(pid), signal.SIGTERM)

        # # -------------------
        # ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        # #
        # # @param arg  the command line argument to parse
        # # @return the parsed command line as required for the platform
        # def split_args(self, arg):
        #     return shlex.split(arg)

    # -------------------
    ## implements the Raspberry Pi specific commands
    class RaspberryPi:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## report current OS
        #
        # @return string indicating OS
        def os_name(self):
            return 'rpi'

        # -------------------
        ## holds OS information
        #
        # @return string indicating OS info
        def os_version(self):
            # TODO confirm this is correct
            return f'RPI {platform.system()} {platform.release()}'

        # # -------------------
        # ## parses the command line into an array of tokens as required by the shell
        # #
        # # @param cmdline the command line to parse
        # # @return an array of elements from the given cmdline
        # def parse_command_line(self, cmdline):
        #     return shlex.split(cmdline)

        # # -------------------
        # ## returns a preexec_fn for Popen calls
        # # not used in Ubuntu implementation
        # #
        # # @return None
        # def preexec_fn(self):
        #     return None

        # # -------------------
        # ## returns the package manager
        # #
        # # @return APT package manager
        # def package_manager(self):
        #     return 'apt'

        # # -------------------
        # ## kill the process group with the given process ID
        # #
        # # @param pid   the process ID to kill
        # # @return None
        # def kill(self, pid):
        #     os.killpg(os.getpgid(pid), signal.SIGTERM)

        # # -------------------
        # ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        # #
        # # @param arg  the command line argument to parse
        # # @return the parsed command line as required for the platform
        # def split_args(self, arg):
        #     return shlex.split(arg)

    # -------------------
    ## initialize
    #
    # selects the current platform and sets impl to it
    # @return None
    @classmethod
    def init(cls):
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
            cls.impl = OsSpecific.RaspberryPi()
        elif sys.platform == 'win32':
            ## holds the implementation class
            cls.impl = OsSpecific.Win()
        elif sys.platform == 'darwin':
            cls.impl = OsSpecific.Mac()
        elif sys.platform == 'linux':
            cls.impl = OsSpecific.Ubuntu()
        else:
            svc.log.bug(f'unrecognized OS: "{sys.platform}"')
            sys.exit(1)

        ## holds the simple OS name: win, ubuntu, macos, rpi
        cls.os_name = cls.impl.os_name()
        ## holds OS information e.g. "ubuntu 20.04 focal"
        cls.os_version = cls.impl.os_version()

        ## holds python version e.g. "3.10"
        cls.python_version = f'Python {sys.version_info.major}.{sys.version_info.minor}'

    # -------------------
    ## get current userid
    #
    # @return userid
    @classmethod
    def userid(cls):
        return getpass.getuser()

    # -------------------
    ## get current hostname
    #
    # @return hostname
    @classmethod
    def hostname(cls):
        return platform.uname().node

    # # -------------------
    # ## parses a command line to be passed into a process start e.g. Popen
    # #
    # # @param cmdline  the command line to parse
    # # @return the parsed command line as required for the platform
    # @classmethod
    # def parse_command_line(cls, cmdline):
    #     return cls.impl.parse_command_line(cmdline)

    # # -------------------
    # ## returns a preexec_fn for Popen calls
    # #
    # # @return the preexec_fn needed for the platform
    # @classmethod
    # def preexec_fn(cls):
    #     return cls.impl.preexec_fn()

    # # -------------------
    # ## returns the name of the package manager
    # #
    # # @return the package manager for the platform
    # @classmethod
    # def package_manager(cls):
    #     return cls.impl.package_manager()

    # # -------------------
    # ## kill the process tree/group with the given process ID
    # #
    # # @param pid   the process ID to kill
    # # @return None
    # @classmethod
    # def kill(cls, pid):
    #     cls.impl.kill(pid)

    # # -------------------
    # ## splits a command line argument into a list of multiple arguments, used in CLI argparse
    # #
    # # @param arg  the command line argument to parse
    # # @return the parsed command line as required for the platform
    # @classmethod
    # def split_args(cls, arg):
    #     return cls.impl.split_args(arg)
