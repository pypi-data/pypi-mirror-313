import gdb
from common import *


@GdbCommandRegistry
class RPC(GdbCommand):
    """
    RPC
    """

    def run(self, arg, from_tty):
        print("Hello \033[0;31;40m RPC \033[0m")
