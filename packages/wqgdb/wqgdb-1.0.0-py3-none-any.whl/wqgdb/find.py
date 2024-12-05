import gdb
from common import *


@GdbCommandRegistry
class Find(GdbCommand):
    """
    find ram.

    usage: wq find addr [debug]
    """

    find_list = []
    heap_used_list = []

    @staticmethod
    def freertos_heap():
        used_list = []
        try:
            xHeapStructSize = GdbValue.get("xHeapStructSize", True)
            if xHeapStructSize:
                _heap_start = (
                    int(GdbValue.get("&_bss_end")) + 4
                )  # int(GdbValue.get("&_heap_start"))
                _heap_end = int(GdbValue.get("&_heap_end"))

                heap_addr = _heap_start
                while heap_addr < _heap_end - int(xHeapStructSize):
                    block = (
                        gdb.Value(heap_addr)
                        .cast(gdb.lookup_type("BlockLink_t").pointer())
                        .dereference()
                    )
                    xBlockSize = int(block["xBlockSize"]) & 0x7FFFFFFF
                    xBlockAllocatedBit = int(block["xBlockSize"]) >> 31
                    heap_addr += xBlockSize
                    if xBlockAllocatedBit:
                        used_list.append((int(block.address), xBlockSize))
        except Exception as e:
            print(e)
        finally:
            # print("freertos_heap", used_list)
            return used_list

    @staticmethod
    def tlsf_heap():
        used_list = []
        g_multi_heap_list = GdbValue.get("g_multi_heap_list")
        for heap in g_multi_heap_list:
            if heap.start != 0x0 and heap.end != 0x0 and heap.heap != 0x0:
                heap_start = int(heap.start)
                heap_end = int(heap.end)
                # print(f"heap start:0x{int(heap_start):X} end:0x{int(heap_end):X}")
                # print(
                #     f"size:{int(heap.heap.pool_size)} free:{int(heap.heap.free_bytes)} min_free:{int(heap.heap.minimum_free_bytes)}"
                # )
                # print(f"heap_data:0x{int(heap.heap.heap_data):X}")

                control = heap.heap.heap_data.cast("control_t*")
                # print(control)
                control_size = GdbValue.get("sizeof(control_t)")
                block_header_size = GdbValue.get("sizeof(control_t)")
                block_header_free_bit = 1 << 0
                block_header_prev_free_bit = 1 << 1
                block_start_offset = 8
                block_header_overhead = 4
                ptr = GdbValue(int(control) + control_size - 4)

                # print(f"ptr:0x{int(ptr):X}")
                while int(ptr) < (heap_end - block_header_size):
                    # print(f"ptr:0x{int(ptr):X}")
                    block = ptr.cast("block_header_t*")
                    # print(block)
                    size = int(block.size) & 0xFFFFFFFC
                    free = True if int(block.size) & block_header_free_bit else False
                    prev_free = (
                        True if int(block.size) & block_header_prev_free_bit else False
                    )
                    # print(f"> 0x{int(block):08X} size:{size} is_free:{free}")
                    ptr = ptr + (size + block_start_offset - block_header_overhead)
                    if free == False:
                        used_list.append((int(block), size))
        # print("tlsf_heap", used_list)
        return used_list

    def find_heap_block(self, addr, deep=0):
        if len(self.heap_used_list) == 0:
            self.heap_used_list = self.freertos_heap()
        if len(self.heap_used_list) == 0:
            self.heap_used_list = self.tlsf_heap()
        if len(self.heap_used_list) == 0:
            return 0

        block_start_offset = 8  # define block_start_offset (offsetof(block_header_t, size) + sizeof(size_t))
        block_header_overhead = 4
        wq_heap_allocate_size = GdbValue.get("sizeof(wq_heap_allocate_t)", True)
        if wq_heap_allocate_size == None:
            wq_heap_allocate_size = 0

        for block_addr, block_size in self.heap_used_list:
            if addr >= (
                block_addr + block_start_offset + int(wq_heap_allocate_size)
            ) and addr <= (block_addr + block_size + block_header_overhead):
                self.print_log(
                    f"{' '*deep*4}{deep} find_heap_block 0x{addr:X} 0x{block_addr:X} 0x{block_size:X} -> {block_addr + block_start_offset + int(wq_heap_allocate_size):X}"
                )
                return block_addr + block_start_offset + int(wq_heap_allocate_size)
        return 0

    def find_bss(self, addr, deep=0, ret=""):
        rets = []
        tasks_addr = GdbValue.get("&tasks")
        tasks_size = GdbValue.get("sizeof(tasks)")
        s = gdb.execute("find &_bss_start,&_bss_end-4,0x%X" % (addr), True, True)
        line = s.replace("\n", " ")
        self.print_log(
            f"{' '*deep*4}{deep} find &_bss_start,&_bss_end-4,0x{addr:X} -> {line}"
        )
        arr = s.strip().split("\n")
        for a in arr:
            if a.startswith("0x"):
                addr = int(a.split(" ")[0], 16)
                if addr < int(tasks_addr) or addr >= (
                    int(tasks_addr) + int(tasks_size)
                ):
                    rets.append(f"{ret} -> {a} ")
                else:
                    print(f"0x{addr:X} ignore tasks")
        return rets

    def find_data(self, addr, deep=0, ret=""):
        rets = []
        s = gdb.execute("find &_data_start,&_data_end-4,0x%X" % (addr), True, True)
        line = s.replace("\n", " ")
        self.print_log(
            f"{' '*deep*4}{deep} find &_data_start,&_data_end-4,0x{addr:X} -> {line}"
        )
        arr = s.strip().split("\n")
        for a in arr:
            if a.startswith("0x"):
                rets.append(f"{ret} -> {a} ")
        return rets

    def find_heap(self, addr, deep=0, ret=""):
        rets = []
        s = gdb.execute("find &_heap_start,&_heap_end,0x%X" % (addr), True, True)
        line = s.replace("\n", " ")
        self.print_log(
            f"{' '*deep*4}{deep} find &_heap_start,&_heap_end,0x{addr:X} -> {line}"
        )
        arr = s.strip().split("\n")
        for a in arr:
            if a.startswith("0x"):
                block = self.find_heap_block(int(a, 16), deep)
                if block:
                    rets += self.find_ram(block, deep + 1, ret)
                    aligned = self.check_heap_aligned_malloc(block)
                    if aligned:
                        rets += self.find_ram(aligned, deep + 1, ret)
        return rets

    def find_tcb(self, tcb, addr):
        s = ""
        # tcb.show()
        if int(tcb) == addr:
            s += tcb.pcTaskName.string()
            # print(f"{int(tcb):x} {int(tcb.pxStack):x} {addr:x}")
        elif int(tcb.pxStack) == addr:
            s += tcb.pcTaskName.string() + " stack"
            # print(f"{int(tcb):x} {int(tcb.pxStack):x} {addr:x}")
        return s

    def find_task_list(self, task_list, addr):
        s = ""
        num = int(task_list.uxNumberOfItems)
        index = task_list.pxIndex

        for i in range(num):
            # print(type(index))
            # print(type(task_list.xListEnd))
            # print(int(index))
            # print(int(task_list.xListEnd.address))
            if index == task_list.xListEnd.address:
                index = index.pxNext
            if index == 0:
                break
            tcb = index.pvOwner.cast("TCB_t*")
            index = index.pxNext
            if tcb == 0:
                continue
            s += self.find_tcb(tcb, addr)
        return s

    def find_task(self, addr):
        s = ""
        for r in GdbValue.parse("pxReadyTasksLists"):
            s += self.find_task_list(r, addr)
        s += self.find_task_list(GdbValue.parse("pxDelayedTaskList"), addr)
        s += self.find_task_list(GdbValue.parse("pxOverflowDelayedTaskList"), addr)
        s += self.find_task_list(GdbValue.parse("xTasksWaitingTermination"), addr)
        s += self.find_task_list(GdbValue.parse("xSuspendedTaskList"), addr)
        return s

    @staticmethod
    def check_heap_aligned_malloc(addr):
        addr = int(addr)
        aligned = [8, 16, 32]
        if addr < int(gdb.parse_and_eval("&_heap_start")) or addr > int(
            gdb.parse_and_eval("&_heap_end")
        ):
            return 0
        for a in aligned:
            addr = (addr + a) & ~(a - 1)
            heap_align = GdbValue(addr - 1).cast("uint8_t*").dereference()
            diff = GdbValue(addr - 2).cast("uint8_t*").dereference()
            # print(f"0x{addr:x} {a} 0x{int(heap_align):x} 0x{int(diff):x}")
            if heap_align == 0x80:
                return addr
        return 0

    def find_ram(self, addr, deep=0, ret=""):
        rets = []
        ret += f"-> 0x{addr:X} "
        if addr in self.find_list:
            self.print_log(f"{' '*deep*4}{deep} ignored {addr:X}")
            return rets
        self.print_log(f"{' '*deep*4}{deep} addr:0x{addr:X}")
        self.find_list.append(addr)
        if deep > 16:
            # print(f"{' '*deep*4} {deep} > 16")
            return rets

        bss = self.find_bss(addr, deep, ret)
        data = self.find_data(addr, deep, ret)
        if len(bss) or len(data):
            rets = bss + data
            return rets

        heap = self.find_heap(addr, deep, ret)
        if len(heap):
            rets = heap
            return rets

        # task = self.find_task(addr)
        # if len(task):
        #     ret += " -> " + task
        #     return ret
        return rets

    def find(self, addr, debug=False):
        self.find_list = []
        self.debug = debug
        info = "\n".join(self.find_ram(addr))
        aligned = self.check_heap_aligned_malloc(addr)
        if aligned:
            info += "\n".join(self.find_ram(aligned))
        return info

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        if len(args) < 1:
            self.print_usage()
            return
        self.debug = True if "debug" in args else False
        print(f"wq find {arg}")
        self.find_list = []
        addr = int(args[0][2:], 16) if args[0].startswith("0x") else int(args[0], 10)
        s = self.find(addr, self.debug)
        print(s)
