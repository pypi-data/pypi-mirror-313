import gdb
from common import *


@GdbCommandRegistry
class Log(GdbCommand):
    """
    print log buffer.
    """

    def run(self, arg, from_tty):
        print("Hello \033[0;31;40m Log \033[0m")
