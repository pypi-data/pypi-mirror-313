import gdb
from common import *


@GdbCommandRegistry
class Task(GdbCommand):
    """
    print all tasks
    """

    @staticmethod
    def print_header():
        print("CPU	 - Processing on CPU number")
        print("TCB	 - task TCB memory address")
        print("TPRI	 - Task priority")
        print("BPRI	 - Base priority")
        print("SS	 - Stack size")
        print("SL	 - Stack limit (available space left)")
        print("RTC	 - time the task has spent in the Running state")
        print("")
        print(
            "CPU    TCB         NAME              STATUS      TPRI  BPRI  MUTEXES_HELD  SS    SL    RTC     "
        )
        print(
            "-----------------------------------------------------------------------------------------------"
        )

    @staticmethod
    def print_task(tcb, status):
        # print(status, tcb)
        stack_size = int(tcb.pxEndOfStack) - int(tcb.pxStack)
        Stack_limit = int(tcb.pxTopOfStack) - int(tcb.pxStack)
        print(
            f"CPU0   0x{int(tcb):08X}  {tcb.pcTaskName.string():16s}  {status: <10.10s}  {int(tcb.uxPriority): <5d} {int(tcb.uxBasePriority): <5d} {int(tcb.uxMutexesHeld): <13d} {stack_size: <5d} {Stack_limit: <5d} {int(tcb.ulRunTimeCounter)}"
        )

    def run(self, arg, from_tty):
        self.print_header()
        for status, taskList in get_task_dict().items():
            for tcb in taskList:
                self.print_task(tcb, status)
