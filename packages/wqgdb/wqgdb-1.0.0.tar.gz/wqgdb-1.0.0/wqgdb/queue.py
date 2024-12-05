import gdb
from common import *


def get_queue(_addr, _type, _debug: bool = False):
    items = []
    os_queue = GdbValue(_addr).cast("os_queue_t*")
    xQueue = os_queue.queue
    if _debug:
        print(os_queue)
        print(xQueue.dereference())
    print(
        f"uxMessagesWaiting:{int(xQueue.uxMessagesWaiting)} uxLength:{int(xQueue.uxLength)} uxItemSize:{int(xQueue.uxItemSize)} \npcHead:0x{int(xQueue.pcHead):x} pcWriteTo:0x{int(xQueue.pcWriteTo):x} pcReadFrom:0x{int(xQueue.u.xQueue.pcReadFrom):x} pcTail:0x{int(xQueue.u.xQueue.pcTail):x}"
    )
    uxMessagesWaiting = int(xQueue.uxMessagesWaiting)
    if uxMessagesWaiting:
        ptr = int(xQueue.u.xQueue.pcReadFrom) + int(xQueue.uxItemSize)
        while uxMessagesWaiting > 0:
            if ptr >= int(xQueue.u.xQueue.pcTail):
                ptr = int(xQueue.pcHead)
            # print(f"0x{ptr:x} cast to {_type}")
            item = GdbValue(int(ptr)).cast(_type + "*").dereference()
            items.append(item)
            ptr += int(xQueue.uxItemSize)
            uxMessagesWaiting -= 1
    return items


@GdbCommandRegistry
class Queue(GdbCommand):
    """
    wq os shim queue.

    usage: wq queue 0x2047b1c app_msg_t*
    """

    full = False

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        print(args)
        _addr = int(args[0][2:], 16)
        _type = "".join(args[1:])
        self.debug = True if "debug" in args else False
        print(f"addr:0x{_addr:x} cast to {_type} type queue")
        items = get_queue(_addr, _type, self.debug)
        for i in items:
            print(i)
        self.full = True if "debug" in args else False

        print("Hello \033[0;31;40m Queue \033[0m")


@GdbCommandRegistry
class Queue_app(GdbCommand):
    """
    print app queue.

    usage: wq queue_app
    """

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        print(args)
        self.debug = True if "debug" in args else False

        hp_queue_handle = GdbValue.get("hp_queue_handle")
        print(f"hp_queue_handle:0x{int(hp_queue_handle):X}")
        items = get_queue(int(hp_queue_handle), "app_msg_t *")
        for i in items:
            if self.debug:
                print(f"p *({str(i.type)})0x{int(i):x}\n", i.dereference())
            else:
                print(
                    f"0x{int(i):x} app msg type:{i['type']} id:{i['id']} priority:{i['priority']} param_len:{i['param_len']}"
                )

        main_queue_handle = GdbValue.get("main_queue_handle")
        print(f"main_queue_handle:0x{int(main_queue_handle):X}")
        items = get_queue(int(main_queue_handle), "app_msg_t *", self.debug)
        for i in items:
            if self.debug:
                print(f"p *({str(i.type)})0x{int(i):x}\n", i.dereference())
            else:
                print(
                    f"0x{int(i):x} app msg type:{i['type'].cast('wq_app_msg_type_t')} id:{i['id']} priority:{i['priority']} param_len:{i['param_len']}"
                )


@GdbCommandRegistry
class Queue_share(GdbCommand):
    """
    print share task queue.

    usage: wq queue_share
    """

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        print(args)
        self.debug = True if "debug" in args else False

        twins_task_faster_queue = GdbValue.get("twins_task.faster.queue")
        print(f"twins_task.faster.queue:0x{int(twins_task_faster_queue):X}")
        items = get_queue(
            int(twins_task_faster_queue), "share_task_queue_item_t", self.debug
        )
        for i in items:
            print(f"p *({str(i.type)}*)0x{int(i.address):x}", i)

        twins_task_slower_queue = GdbValue.get("twins_task.slower.queue")
        print(f"twins_task.slower.queue:0x{int(twins_task_slower_queue):X}")
        items = get_queue(
            int(twins_task_slower_queue), "share_task_queue_item_t", self.debug
        )
        for i in items:
            print(f"p *({str(i.type)}*)0x{int(i.address):x}", i)


@GdbCommandRegistry
class Queue_as(GdbCommand):
    """
    print audio service queue.

    usage: wq queue_as
    """

    def run(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        print(args)
        self.debug = True if "debug" in args else False
        aud_sv_env_msg_q = GdbValue.get("aud_sv_env.msg_q", True)
        if aud_sv_env_msg_q:
            print(f"aud_sv_env_msg_q:0x{int(aud_sv_env_msg_q):X}")
            items = get_queue(int(aud_sv_env_msg_q), "aud_sv_msg_t", self.debug)

            for i in items:
                if self.debug:
                    print(f"p *({str(i.type)}*)0x{int(i.address):x}", i)
                    if int(i.evt_id) == int(gdb.parse_and_eval("AS_MSG_ASRC_IO_CB")):
                        p_dmsg = i.data.cast("dtop_asrc_cb_msg_t*")
                        print(p_dmsg)
                else:
                    print(
                        f"0x{int(i.address):x} msg_id:{i.msg_id.cast('enum TASK_EVT_ID')} evt_id:{int(i.evt_id)}"
                    )
                    if int(i.evt_id) == int(gdb.parse_and_eval("AS_MSG_ASRC_IO_CB")):
                        p_dmsg = i.data.cast("dtop_asrc_cb_msg_t*")
                        print(
                            f"    evt:{int(p_dmsg.evt)} path:{p_dmsg.path} is_asrc_tx_ok:{int(p_dmsg.is_asrc_tx_ok)}"
                        )

                    if int(i.evt_id) == int(gdb.parse_and_eval("AS_MSG_SPK_FEEDBACK")):
                        p_dmsg = i.data.cast("dtop_feedback_msg_t*")
                        print(f"    evt:{int(p_dmsg.evt)}")

                    if int(i.evt_id) == int(gdb.parse_and_eval("AS_MSG_ASRC")):
                        p_dmsg = i.data.cast("dtop_asrc_msg_t*")
                        print(
                            f"    channel_id:{int(p_dmsg.channel_id)} reason:{int(p_dmsg.reason)} cnt:{int(p_dmsg.cnt)} path:{int(p_dmsg.path)}"
                        )

                    # if int(i.evt_id) == int(gdb.parse_and_eval("AS_MSG_RECORD")):
                    #     p_dmsg = i.data.cast("dtop_record_msg_t*")
                    #     print(
                    #         f"    streamid:{int(p_dmsg.streamid)} remoteid:{int(p_dmsg.remoteid)} addr:{int(p_dmsg.addr)} len:{int(p_dmsg.len)} mic_map:{int(p_dmsg.mic_map)} ts:{int(p_dmsg.ts)}"
                    #     )
