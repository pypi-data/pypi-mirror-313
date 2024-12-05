import gdb
from common import *


@GdbCommandRegistry
class WDT(GdbCommand):
    """
    WDT
    """

    def run(self, arg, from_tty):
        print("Hello \033[0;31;40m WDT \033[0m")
