import gdb
from common import *


@GdbCommandRegistry
class trace(GdbCommand):
    """
    freertos trace

    req: wqcore cherry-pick 899c5cddb727b16ba0d9f5102174d8a7fe30c6da
    """

    def run(self, arg, from_tty):
        tcb_list = get_task_list()
        os_trace = GdbValue.get("os_trace")
        os_trace_event_size = int(GdbValue.get("sizeof(os_trace_event_t)"))
        os_trace_size = int(
            (int(GdbValue.get("sizeof(os_trace)")) - 4) / os_trace_event_size
        )
        os_trace_idx = os_trace.event_idx
        range_list = list(range(os_trace_idx - 1, 0 - 1, -1))
        range_list += list(range(os_trace_size - 1, os_trace_idx - 1, -1))
        next_ts = 0
        run_ms = 0
        for i in range_list:
            event = os_trace.event_buf[i]
            event_id = str(event.id.cast('os_trace_event_id_t'))
            tcb = int(event.tcb) | 0x02000000
            name = ""
            for t in tcb_list:
                if int(t) == tcb:
                    name = t.pcTaskName.string()

            if next_ts != 0:
                run_ms = ((next_ts - int(event.ts))/31.25)

            print(
                f"{i:03d} 0x{tcb:08X} {name:16s} {event_id:32s} {(int(event.ts)/31.25):09.3f}ms run:{run_ms:09.3f}ms"
            )
            next_ts = int(event.ts)
