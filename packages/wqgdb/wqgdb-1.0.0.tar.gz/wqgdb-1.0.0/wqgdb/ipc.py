import gdb
from common import *


@GdbCommandRegistry
class IPC(GdbCommand):
    """
    IPC

    wq_ipc_send_msg -> wq_ipc_write_mailbox -> intc_send_software_int -> machine_soft_interrupt_handler -> wq_ipc_recv_message -> call port handler
    """

    WQ_CORES_ACORE = 0
    WQ_CORES_BCORE = 1
    WQ_CORES_DCORE = 2

    def print_ipc_msg(self, msg, core: int, index: int = 0, box: int = 0):
        '''
        typedef struct msg {
            uint32_t dst_port    : 10; /*!< destination port*/
            uint32_t src_port    : 10; /*!< source port */
            uint32_t payload_len : 10; /*!< payload length */
            uint32_t break_off   : 1;  /*!< whether to be break off */
            uint32_t reserved    : 1;  /*!< unused */
            uint8_t payload[];         /*!< message body */
        } ipc_msg_t;
        '''
        name = str(core) + "_" + str(msg.dst_port)
        # print(name, self.ipc_named_port_dict)
        named_port = (
            self.ipc_named_port_dict[name]
            if name in self.ipc_named_port_dict.keys()
            else ""
        )
        payload_addr = int(msg.payload.address)
        if msg.break_off:
            payload_addr = box
        print(
            f"index:{index} ipc msg:0x{int(msg):08X} dst_port:{msg.dst_port} {named_port} src_port:{msg.src_port} payload_len:{msg.payload_len} payload_addr:0x{payload_addr:08X} break_off:{msg.break_off}"
        )
        # if self.debug:
        #     print(f"p *(ipc_msg_t*)0x{int(msg):08X} {str(msg)}")

    def print_mailbox_data(self, mbox, core: int):
        ipc_msg_size = int(GdbValue.get("sizeof(ipc_msg_t)"))
        if self.debug:
            print(f"p *(wq_ipc_mailbox_t*)0x{int(mbox):08X} {str(mbox)}")

        print(
            f"mailbox:0x{int(mbox):08X} size:{int(mbox.size)} w:{int(mbox.w)} r:{int(mbox.r)} data:0x{int(mbox.data.address):08X}"
        )

        if self.full:
            print("-----------------------------full------------------------")
            index = 0
            last_index = 0
            while index < int(mbox.size):
                addr = int(mbox.data.cast("uint32_t")) + index
                msg = GdbValue(addr).cast("ipc_msg_t*")
                if self.debug:
                    print(f"index:{index} {str(msg)}")
                if (
                    msg.dst_port < 16
                    and msg.src_port < 16
                    and msg.payload_len <= int(mbox.size)
                ):
                    self.print_ipc_msg(msg, core, index, int(mbox.data.address))
                index += ipc_msg_size
        else:
            if mbox.w > mbox.r:
                index = int(mbox.r)
                while index < mbox.w:
                    addr = int(mbox.data.cast("uint32_t")) + index
                    msg = GdbValue(addr).cast("ipc_msg_t*")
                    print(f"index:{index}")
                    self.print_ipc_msg(msg, core, index, int(mbox.data.address))
                    index += ipc_msg_size + int(msg.payload_len)
            else:
                index = int(mbox.r)
                while index < mbox.w or (index > mbox.w and index < mbox.size):
                    addr = int(mbox.data.cast("uint32_t")) + index
                    msg = GdbValue(addr).cast("ipc_msg_t*")
                    print(f"index:{index} {str(msg)}")
                    self.print_ipc_msg(msg, core, index, int(mbox.data.address))
                    if msg.break_off:
                        index = int(msg.payload_len)
                    else:
                        index += ipc_msg_size + int(msg.payload_len)
                    if index >= mbox.size:
                        index = 0

    def print_port_ctrl(self):
        '''
        typedef struct ipc_port_handler_group {
            struct ipc_port_handler_group *next;
            wq_ipc_handler handler[WQ_IPC_PORT_GROUP_MAX_CNT];
            uint16_t port_start;
            uint16_t port_end;
        } ipc_port_handler_group_t;

        typedef struct ipc_port_handler_ctrl {
            ipc_port_handler_group_t *head;
            ipc_port_handler_group_t *tail;
            uint16_t port_index;
        } ipc_port_handler_ctrl_t;
        '''
        port_ctrl = GdbValue.get("port_ctrl")
        print(f"port_ctrl.port_index:{port_ctrl.port_index}")
        phg = port_ctrl.head
        while phg != 0:
            print(f"0x{int(phg):08X} port_start:{int(phg.port_start)} port_end:{int(phg.port_end)}")
            if self.debug:
                print(f"p *(ipc_port_handler_group_t*)0x{int(phg):08X} {str(phg)}")
            phg = phg.next

    def print_ipc_ctrl(self):
        '''
        /**
        * @brief Mailbox heaader
        */
        typedef struct mailbox {
            uint32_t size;  /*!< size of the mailbox */
            uint16_t w;     /*!< write index */
            uint16_t r;     /*!< read index */
            uint8_t data[]; /*!< ring data buffer */
        } wq_ipc_mailbox_t;

        /**
        * @brief IPC mailbox control. Record the mailbox addresses of all cores.
        */
        typedef struct ipc_ctrl {
            uint32_t magic;                                     /*!< Magic for valid check */
            volatile wq_ipc_mailbox_t
                *mailbox[WQ_CORES_EN_MAX][WQ_CORES_EN_MAX - 1]; /*!< mailbox addresses */
            volatile struct list_head ipc_named_port_list;
        } wq_ipc_ctrl_t;
        '''
        ipc_ctrl = GdbValue.get("ipc_ctrl")
        if ipc_ctrl.magic != 0x57514943:
            print(f"ipc_ctrl.magic {ipc_ctrl.magic} != 0x57514943.")
            return

        # print(ipc_ctrl)
        print("ipc_named_port_list")
        self.ipc_named_port_dict = {}
        ipc_named_port_list = ipc_ctrl.ipc_named_port_list
        for np in wq_generic_list(ipc_named_port_list, "ipc_named_port_t*"):
            # print(f"p *(ipc_named_port_t*)0x{int(np.address):08X} = {str(np)}")
            print(
                f"name:{np.name.string():32s} port:{int(np.port):04d} core:{int(np.core)} {np.core.cast('WQ_CORES')}"
            )
            self.ipc_named_port_dict[str(int(np.core)) + "_" + str(int(np.port))] = (
                np.name.string()
            )

        mbox = ipc_ctrl.mailbox[self.WQ_CORES_ACORE][0]
        print(f"mailbox bcore write -> acore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_ACORE)

        mbox = ipc_ctrl.mailbox[self.WQ_CORES_ACORE][1]
        print(f"mailbox dcore write -> acore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_ACORE)

        mbox = ipc_ctrl.mailbox[self.WQ_CORES_BCORE][0]
        print(f"mailbox acore write -> bcore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_BCORE)
        mbox = ipc_ctrl.mailbox[self.WQ_CORES_BCORE][1]
        print(f"mailbox dcore write -> bcore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_BCORE)

        mbox = ipc_ctrl.mailbox[self.WQ_CORES_DCORE][0]
        print(f"mailbox acore write -> dcore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_DCORE + 2)
        mbox = ipc_ctrl.mailbox[self.WQ_CORES_DCORE][1]
        print(f"mailbox bcore write -> dcore read")
        self.print_mailbox_data(mbox, self.WQ_CORES_DCORE + 2)

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        # print(args)
        self.debug = True if "debug" in args else False
        self.full = True if "full" in args else False
        self.print_port_ctrl()
        self.print_ipc_ctrl()
