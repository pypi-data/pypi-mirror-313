import gdb
from common import *


@GdbCommandRegistry
class DFS(GdbCommand):
    """
    print dfs.

    usage: wq dfs
    """

    def run(self, arg, from_tty):
        dfs_env = GdbValue.get("dfs_env")
        print(dfs_env)
