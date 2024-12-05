import gdb
from common import *


@GdbCommandRegistry
class PM(GdbCommand):
    """
    print power manage device list.

    usage: wq pm
    """

    def run(self, arg, from_tty):
        pm_device_list = GdbValue.get("pm_device_list")
        print(
            f"pm_device_list\np *(struct list_head*)0x{int(pm_device_list.address):08X} = {str(pm_device_list)}"
        )
        for dev in wq_generic_list(pm_device_list, "pm_device_t*"):
            print(f"p *(pm_device_t*)0x{int(dev.address):08X} = {str(dev)}")
