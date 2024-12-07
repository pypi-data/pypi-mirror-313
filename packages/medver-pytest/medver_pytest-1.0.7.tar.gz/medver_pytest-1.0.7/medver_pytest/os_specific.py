import os
import sys


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

    ## holds a reference to the implementation class for the current OS
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
    ## implements the Mac specific commands
    class Mac:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'macos'

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
    ## initialize
    #
    # selects the current platform and sets impl to it
    # @return None
    @classmethod
    def init(cls):
        ## holds the implementation class
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
            cls.impl = OsSpecific.RaspberryPi()
        elif sys.platform == 'win32':
            cls.impl = OsSpecific.Win()
        elif sys.platform == 'darwin':
            cls.impl = OsSpecific.Mac()
        elif sys.platform == 'linux':
            cls.impl = OsSpecific.Ubuntu()
        else:
            print(f'ERR: unrecognized OS: "{sys.platform}"')
            sys.stdout.flush()
            sys.exit(1)

        ## holds the simple OS name: win, ubuntu, macOS, rpi
        cls.os_name = cls.impl.os_name()
