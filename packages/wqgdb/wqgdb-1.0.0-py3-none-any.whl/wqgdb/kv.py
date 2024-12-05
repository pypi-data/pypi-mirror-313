import gdb
from common import *


@GdbCommandRegistry
class KV(GdbCommand):
    """
    print Key Value cache list.

    usage: wq kv
    """

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        # print(args)
        self.debug = True if "debug" in args else False
        key_value_cache_st = GdbValue.get("key_value_cache_st")
        print(f"key_value_cache_st = {str(key_value_cache_st)}")
        read_list = key_value_cache_st.read_list
        write_list = key_value_cache_st.write_list
        print(
            f"key_value_cache_st.read_list\np *(struct list_head*)0x{int(read_list.address):08X} = {str(read_list)}"
        )

        for p in wq_generic_list(read_list, "key_value_cached_key_t*"):
            if self.debug:
                print(f"p *(key_value_cached_key_t*)0x{int(p.address):08X} = {str(p)}")
            else:
                print(
                    f"id:0x{int(p.id):04X}={int(p.id):<5d} length:{int(p.length):<5d} data:0x{int(p.data.address):08X}"
                )
        print(
            "-----------------------------------------------------------------------------------"
        )
        print(
            f"key_value_cache_st.write_list\np *(struct list_head*)0x{int(write_list.address):08X} = {str(write_list)}"
        )

        for p in wq_generic_list(write_list, "key_value_cached_key_t*"):
            if self.debug:
                print(f"p *(key_value_cached_key_t*)0x{int(p.address):08X} = {str(p)}")
            else:
                print(
                    f"id:0x{int(p.id):04X}={int(p.id):<5d} length:{int(p.length):<5d} data:0x{int(p.data.address):08X}"
                )
