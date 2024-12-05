import gdb
from common import *


@GdbCommandRegistry
class Timer(GdbCommand):
    """
    print all timer

    usage: wq timer
    """

    @staticmethod
    def print_header():
        print(f"          interval  trigger  current  status fn                  ")
        print(f"-------------------------------------------------------------------")

    @staticmethod
    def print_timer(timer):
        # print(timer)
        arg = timer.pvTimerID.cast("wrapper_timer_arg_t*")
        # print(arg)
        status = "active" if (int(timer.ucStatus) & 0x01) else "!active"
        print(
            f"{int(timer):#08x} {int(timer.xTimerPeriodInTicks):8d} {int(timer.xTimerListItem.xItemValue):8d} {xTaskGetTickCount():8d} {status:>7s} {str(arg.fn)} "
        )

    def run(self, arg, from_tty):
        _current = GdbValue.get("xActiveTimerList1")
        _overflow = GdbValue.get("xActiveTimerList2")
        _current_list = FreeRtosList(_current, "Timer_t")
        _overflow_list = FreeRtosList(_overflow, "Timer_t")
        self.print_header()
        for timer in _current_list:
            self.print_timer(timer)
        for timer in _overflow_list:
            self.print_timer(timer)
