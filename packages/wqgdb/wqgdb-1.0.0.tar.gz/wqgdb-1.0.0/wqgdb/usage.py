import gdb
from common import *


@GdbCommandRegistry
class Usage(GdbCommand):
    """
    print usage

    usage: wq usage
    """

    def run(self, arg, from_tty):
        tatol_size, free, lowest = get_heap_size()
        tcb_list = get_task_list()
        ulTaskSwitchedInTime = GdbValue.get("ulTaskSwitchedInTime")

        if GdbValue.get("cpu_usage_env", True):  # ADK
            cpu_usage_env = GdbValue.get("cpu_usage_env")
            now = cpu_usage_env.now
            last = cpu_usage_env.last
            # reverse
            tmp = last
            last = now
            now = tmp

            ts_span = int(ulTaskSwitchedInTime) - int(now.ts)

            print(
                f"Mem total:{tatol_size} free:{free} lowest:{lowest} ts_span:{ts_span}({wq_rtc_to_ms(ts_span)}ms)"
            )
            print("No. Thread name            Cycle           %%    Pri stack lowest")
            print("-----------------------------------------------------------------")
            for i in range(now.num):
                now_task = now.task_array[i]
                for t in tcb_list:
                    if t.uxTCBNumber == now_task.id:
                        break
                task_ts_span = int(t.ulRunTimeCounter) - int(now_task.cpu_ts)
                radio = int(task_ts_span * 100 / ts_span)
                print(
                    f"{i + 1:3d} {now_task.name.string():16s} {int(task_ts_span):>8d}({wq_rtc_to_ms(task_ts_span):<7.2f}ms) {radio:3d}%   {int(now_task.priority):2d}  {int(now_task.stack_size):10d}(W)"
                )

        elif GdbValue.get("g_cpu_usage_ctxt", True):  # opencore
            cpu_usage_env = GdbValue.get("g_cpu_usage_ctxt")
            now = cpu_usage_env.start
            last = cpu_usage_env.end
            # reverse
            tmp = last
            last = now
            now = tmp

            ts_span = int(ulTaskSwitchedInTime) - int(now.ts)

            print(
                f"Mem total:{tatol_size} free:{free} lowest:{lowest} ts_span:{ts_span}({wq_rtc_to_ms(ts_span)}ms)"
            )
            print("No. Thread name            Cycle           %%    Pri stack lowest")
            print("-----------------------------------------------------------------")
            for i in range(now.num):
                now_task = now.p_tasks[i]
                for t in tcb_list:
                    if t.uxTCBNumber == now_task.id:
                        break
                task_ts_span = int(t.ulRunTimeCounter) - int(now_task.cpu_ts)
                radio = int(task_ts_span * 100 / ts_span)
                print(
                    f"{i + 1:3d} {now_task.name.string():16s} {int(task_ts_span):>8d}({wq_rtc_to_ms(task_ts_span):<7.2f}ms) {radio:3d}%   {int(now_task.priority):2d}  {int(now_task.stack_size):10d}(W)"
                )
