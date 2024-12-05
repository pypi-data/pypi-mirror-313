import gdb
from common import *


@GdbCommandRegistry
class Heap5(GdbCommand):
    """
    freertos heap5.
    """

    def run(self, arg, from_tty):
        # dd = GdbValue.parse("&_heap_end")
        # print(dd.test_att)
        _heap_end = int(GdbValue.parse("&_heap_end"))

        try:
            _heap_start = int(GdbValue.parse("&_heap_start"))
        except Exception as e:
            print(e)
            _heap_start = int(GdbValue.parse("&_bss_end")) + 4

        try:
            xHeapStructSize = int(GdbValue.parse("xHeapStructSize"))
        except Exception as e:
            print(e)
            xHeapStructSize = 8

        heap_tatol_size = int(GdbValue.parse("heap_tatol_size"))
        xBlockAllocatedBit = int(GdbValue.parse("xBlockAllocatedBit"))
        xFreeBytesRemaining = int(GdbValue.parse("xFreeBytesRemaining"))
        xMinimumEverFreeBytesRemaining = int(
            GdbValue.parse("xMinimumEverFreeBytesRemaining")
        )

        print(
            f"heap0 start_addr:0x{_heap_start:X} end_addr:0x{_heap_end:X} size:0x{(_heap_end - _heap_start):X}",
        )
        print(
            f"heap_tatol_size:0x{heap_tatol_size:X} xFreeBytesRemaining:0x{xFreeBytesRemaining:X} xMinimumEverFreeBytesRemaining:0x{xMinimumEverFreeBytesRemaining:X}",
        )
        used_list = {}
        free_list = {}
        heap_addr = _heap_start
        while heap_addr < _heap_end - xHeapStructSize:
            block = (
                gdb.Value(heap_addr)
                .cast(gdb.lookup_type("BlockLink_t").pointer())
                .dereference()
            )
            xBlockSize = int(block["xBlockSize"]) & 0x7FFFFFFF
            xBlockAllocatedBit = int(block["xBlockSize"]) >> 31
            # print(block)
            # print(
            #     f"offset:0x{int(block.address):X} pxNextFreeBlock:{int(block['pxNextFreeBlock']):X} xBlockSize:{xBlockSize} xBlockAllocatedBit:{xBlockAllocatedBit}"
            # )
            if xBlockAllocatedBit:
                if xBlockSize not in used_list.keys():
                    used_list[xBlockSize] = [block]
                else:
                    used_list[xBlockSize].append(block)
            else:
                if xBlockSize not in free_list.keys():
                    free_list[xBlockSize] = [block]
                else:
                    free_list[xBlockSize].append(block)
            heap_addr += xBlockSize
        print("used:")
        self.used_list = sorted(
            used_list.items(), key=lambda x: len(x[1]) * int(x[0]), reverse=True
        )
        for k, v in self.used_list:
            print(f"size:{k} count:{len(v)}")
            f = find()
            for block in v:
                data_addr = int(block.address) + xHeapStructSize
                heap_trace = GdbValue(
                    gdb.Value(data_addr)
                    .cast(gdb.lookup_type("heap_dbg_block_trace_t").pointer())
                    .dereference()
                )
                # print(heap_trace)
                print(
                    "    0x%08X ra:0x%08X rtc:%d"
                    % (
                        int(heap_trace.address),
                        int(heap_trace.ra),
                        int(heap_trace.rtc),
                    )
                )
                data_addr += int(GdbValue.parse("sizeof(heap_dbg_block_trace_t)"))
                info = f.find_ram(data_addr)
                print(f"data_addr:0x{data_addr:X} {info}")

        print("free:")
        self.free_list = sorted(
            free_list.items(), key=lambda x: len(x[1]) * int(x[0]), reverse=True
        )
        for k, v in self.free_list:
            print(f"size:{k} count:{len(v)}")


@GdbCommandRegistry
class TLSF(GdbCommand):
    """
    wq tlsf.

    usage: wq tlsf [full] [find]
    """

    def get_heap_list(self):
        used_list = []
        free_list = []
        used_dict = {}
        free_dict = {}
        g_multi_heap_list = GdbValue.get("g_multi_heap_list")
        for heap in g_multi_heap_list:
            if heap.start != 0x0 and heap.end != 0x0 and heap.heap != 0x0:
                heap_start = int(heap.start)
                heap_end = int(heap.end)
                print(f"heap start:0x{int(heap_start):X} end:0x{int(heap_end):X}")
                print(
                    f"size:{int(heap.heap.pool_size)} free:{int(heap.heap.free_bytes)} min_free:{int(heap.heap.minimum_free_bytes)}"
                )
                print(f"heap_data:0x{int(heap.heap.heap_data):X}")

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
                    if self._full:
                        print(
                            f"block:0x{int(block):08X} size:{size:05d} is_free:{free} prev_free:{prev_free}"
                        )
                    if self._find and free == False:
                        wq_heap_allocate_size = GdbValue.get(
                            "sizeof(wq_heap_allocate_t)", True
                        )
                        if wq_heap_allocate_size:
                            heap_trace = (block.cast("uint8_t*") + 8).cast(
                                "wq_heap_allocate_t*"
                            )
                            # print(heap_trace)
                            print(
                                f"trace:0x{int(heap_trace):08X} rtc:{int(heap_trace.rtc)} ra:0x{int(heap_trace.ra):08X} task_handle:0x{int(heap_trace.task_handle):08X}"
                            )
                            addr = int(block) + 8 + int(wq_heap_allocate_size)
                        else:
                            addr = int(block) + 8

                        gdb.execute(f"wq find 0x{addr:08X}")

                    ptr = ptr + (size + block_start_offset - block_header_overhead)
                    if free:
                        if size not in free_dict.keys():
                            free_dict[size] = [block]
                        else:
                            free_dict[size].append(block)
                    else:
                        if size not in used_dict.keys():
                            used_dict[size] = [block]
                        else:
                            used_dict[size].append(block)

        free_list = sorted(
            free_dict.items(), key=lambda x: len(x[1]) * int(x[0]), reverse=True
        )
        used_list = sorted(
            used_dict.items(), key=lambda x: len(x[1]) * int(x[0]), reverse=True
        )
        return used_list, free_list

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        self._full = True if "full" in args else False
        self._find = True if "find" in args else False
        used_list, free_list = self.get_heap_list()
        print("free:")
        for k, v in free_list:
            print(f"size:{k} count:{len(v)}")

        print("used:")
        heap_used_list = [(int(b), k) for k, v in used_list for b in v]

        for k, v in used_list:
            print(f"size:{k} count:{len(v)}")
