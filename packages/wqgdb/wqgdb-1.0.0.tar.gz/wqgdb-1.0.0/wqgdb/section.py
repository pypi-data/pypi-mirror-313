import gdb
from common import *


@GdbCommandRegistry
class Section(GdbCommand):
    """
    print section.
    """

    def run(self, arg, from_tty):
        _iram_text_start = int(gdb.parse_and_eval("&_iram_text_start"))
        _iram_text_end = int(gdb.parse_and_eval("&_iram_text_end"))
        _iram_text_size = _iram_text_end - _iram_text_start
        _data_start = int(gdb.parse_and_eval("&_data_start"))
        _data_end = int(gdb.parse_and_eval("&_data_end"))
        _data_size = _data_end - _data_start
        _bss_start = int(gdb.parse_and_eval("&_bss_start"))
        _bss_end = int(gdb.parse_and_eval("&_bss_end"))
        _bss_size = _bss_end - _bss_start
        _heap_start = int(gdb.parse_and_eval("&_heap_start"))
        _heap_end = int(gdb.parse_and_eval("&_heap_end"))
        _heap_size = _heap_end - _heap_start
        __stack_size = int(gdb.parse_and_eval("&__stack_size"))
        __stack_top = int(gdb.parse_and_eval("&__stack_top"))
        stack_end = __stack_top - __stack_size
        print(
            f"_iram_start:0x{_iram_text_start:08X}    _iram_end:0x{_iram_text_end:08X}     iram_size:{_iram_text_size}"
        )
        print(
            f"_data_start:0x{_data_start:08X}    _data_end:0x{_data_end:08X}     data_size:{_data_size}"
        )
        print(
            f" _bss_start:0x{_bss_start:08X}     _bss_end:0x{_bss_end:08X}      bss_size:{_bss_size}"
        )
        print(
            f"_heap_start:0x{_heap_start:08X}    _heap_end:0x{_heap_end:08X}    stack_size:{_heap_size}"
        )
        print(
            f"  stack_end:0x{stack_end:08X}  __stack_top:0x{__stack_top:08X}  __stack_size:{__stack_size}"
        )
