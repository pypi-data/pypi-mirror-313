import gdb
from common import *


@GdbCommandRegistry
class Stack(GdbCommand):
    """
    dispaly stack info. usage: wq stack [full]
    """

    @staticmethod
    def prvTaskCheckFreeStackSpace(pucStackByte: int) -> int:
        """
        static configSTACK_DEPTH_TYPE prvTaskCheckFreeStackSpace( const uint8_t *pucStackByte )
        {
            uint32_t ulCount = 0U;

            while ( *pucStackByte == ( uint8_t ) tskSTACK_FILL_BYTE ) {
                pucStackByte -= portSTACK_GROWTH;
                ulCount++;
            }

            ulCount /= ( uint32_t ) sizeof( StackType_t ); /*lint !e961 Casting is not redundant on smaller architectures. */

            return ( configSTACK_DEPTH_TYPE ) ulCount;
        }
        """
        ulCount = 0
        addr = pucStackByte
        for _ in range(1000):
            value = GdbValue(addr).cast("uint32_t*").dereference()
            addr += 4
            if value == 0xA5A5A5A5:
                ulCount += 1
            else:
                break
        return ulCount

    def get_func_name(self, pc: int) -> str:
        s = gdb.execute(f'info symbol 0x{pc:08X}',to_string=True)
        if s.find('.iram_text') >= 0 or s.find('.text') >= 0 or s.find('.rom_text') >= 0:
            return s.split(' ')[0]
        else:
            return ""
        
        ## Searching with block_for_pc will be missing some functions
        # block = gdb.block_for_pc(pc)
        # print(block)
        # if block and block.function:
        #     return block.function.name
        # else:
        #     return ""

    def print_stack(self, top: int, size: int, sp: int):
        bottom = top - size
        addr = top
        # print(f"stack top:0x{top:08X} size:0x{size:08X} sp:0x{sp:08X}")
        print(
            f"{colors['blue']} offset     | stack_addr:func_addr  -> function       {color_reset}"
        )
        print(
            f"{colors['blue']} ---------------------------------------------------- {color_reset}"
        )
        try:
            while addr >= bottom:
                addr -= 4
                # print(f"addr:{addr:#08X}")
                if addr >= sp or self.full:
                    value = int(GdbValue(addr).cast("uint32_t*").dereference())
                    # print(f"value:{int(value):#08X}")
                    if name := self.get_func_name(value):
                        print(
                            f" 0x{(top-addr):08X} | 0x{addr:08X}:0x{int(value):08X} -> {name} ↓"
                        )
                if addr == sp:
                    print(f" ----------------------------------------------------")
        except Exception as e:
            print(e)

    def print_isr_stack(self):
        top = int(GdbValue.get("&__stack_top"))
        size = int(GdbValue.get("&__stack_size"))
        bottom = top - size

        print(
            f"sp:N/A top:0x{top:08X} bottom:0x{bottom:08X} size:0x{size:08X}(B) isr stack"
        )
        self.print_stack(top, size, top - size)

    def print_task_stack(self):
        pxCurrentTCB = GdbValue.get("pxCurrentTCB")
        for tcb in get_task_list():
            name = tcb.pcTaskName.string()
            top = int(tcb.pxTopOfStack)
            start = int(tcb.pxStack)
            end = int(tcb.pxEndOfStack)
            lowest = self.prvTaskCheckFreeStackSpace(start)
            if lowest == 0:
                print(f"{colors['red']}  {name} stack overflow {color_reset}")
            if int(pxCurrentTCB) == int(tcb):
                print(
                    f"\n{colors['yellow']} sp:0x{top:08X} top:0x{end:08X} bottom:0x{start:08X} size:0x{end - start:08X}(B) lowest:0x{lowest*4:08X}(B) {name}(CurrentTCB) {color_reset}"
                )
            else:
                print(
                    f"\n{colors['green']} sp:0x{top:08X} top:0x{end:08X} bottom:0x{start:08X} size:0x{end - start:08X}(B) lowest:0x{lowest*4:08X}(B) {name} {color_reset}"
                )
            self.print_stack(end, end - start, top)

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        # print(args)
        self.full = True if "full" in args else False
        self.print_isr_stack()
        self.print_task_stack()
