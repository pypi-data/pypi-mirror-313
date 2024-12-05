import gdb
import traceback

colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
color_reset = "\033[0m"


class GdbCommandRegistry:
    classes = {}

    def __init__(self, cls):
        self.classes[cls.__name__] = cls


class GdbCommand(gdb.Command):
    """
    gdb command base.
    """

    def __init__(self):
        super().__init__("wq " + self.__class__.__name__.lower(), gdb.COMMAND_USER)
        self.debug = False

    def print_usage(self):
        print(self.__doc__)

    def print_log(self, log, *args, **kwargs):
        if self.debug:
            print(log)

    def run(self, arg, from_tty):
        print("GDB Command Base.")

    def invoke(self, arg, from_tty):
        try:
            self.run(arg, from_tty)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


class GdbValue(gdb.Value):
    def __init__(self, val):
        super(GdbValue, self).__init__(val)

    def __str__(self):
        # print(f"__str__", self.type.code, str(self.type))
        if self.type.code == gdb.TYPE_CODE_PTR:
            return self.dereference().format_string(raw=False, styling=True)
        else:
            return self.format_string(raw=False, styling=True)

    def __eq__(self, other):
        # print(f"__eq__", type(self), str(self.type), other)
        if isinstance(other, str):
            return self.string() == other
        elif isinstance(other, gdb.Value):
            return int(other) == int(self)
        elif isinstance(other, GdbValue):
            return int(other) == int(self)
        else:
            return other == int(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return GdbValue(super(GdbValue, self).__add__(other))

    def __sub__(self, other):
        return GdbValue(super(GdbValue, self).__sub__(other))

    def __mul__(self, other):
        return GdbValue(super(GdbValue, self).__mul__(other))

    def __truediv__(self, other):
        return GdbValue(super(GdbValue, self).__truediv__(other))

    def __mod__(self, other):
        return GdbValue(super(GdbValue, self).__mod__(other))

    def __and__(self, other):
        return GdbValue(super(GdbValue, self).__and__(other))

    def __or__(self, other):
        return GdbValue(super(GdbValue, self).__or__(other))

    def __xor__(self, other):
        return GdbValue(super(GdbValue, self).__or__(other))

    def __lshift__(self, other):
        return GdbValue(super(GdbValue, self).__lshift__(other))

    def __rshift__(self, other):
        return GdbValue(super(GdbValue, self).__rshift__(other))

    def __int__(self):
        # print(f"__int__ {str(self.type)} {self.type.sizeof}")
        return super(GdbValue, self).__int__()

    def __add__(self, other):
        return GdbValue(super(GdbValue, self).__add__(other))

    def __iter__(self):
        index = 0
        while True:
            # print(f"__iter__ {index} {str(self.type)} {self.type.code}")
            if self.type.code != gdb.TYPE_CODE_ARRAY:
                break
            r = self.type.range()
            if index >= (r[1] + 1):
                break
            yield self[index]
            index += 1

    def __getitem__(self, key):
        # print(f"__getitem__ {key} {type(key)} {str(self.type)} {self.type.code}")
        return GdbValue(super(GdbValue, self).__getitem__(key))

    def __getattribute__(self, attr_name):
        if attr_name in ["__dict__", "__members__", "__methods__", "__class__"]:
            # print(f"1__getattribute__ {attr_name}")
            return object.__getattribute__(self, attr_name)
        elif attr_name in dir(self.__class__):
            # print(f"2__getattribute__ {attr_name}")
            return super(GdbValue, self).__getattribute__(attr_name)
        elif self.type.code == gdb.TYPE_CODE_PTR:
            # print(f"3__getattribute__ {attr_name}")
            # print(self.type.code,str(self.type))
            return GdbValue(self.dereference()[attr_name])
        else:
            # print(f"4__getattribute__ {attr_name}")
            # print(self.type.code,str(self.type))
            return GdbValue(self[attr_name])

    def cast(self, t):
        if isinstance(t, gdb.Type):
            return GdbValue(super(GdbValue, self).cast(t))
        elif isinstance(t, str):
            t = t.replace("(", "").replace(")", "").strip()
            if t.endswith("**"):
                return GdbValue(
                    super(GdbValue, self).cast(
                        gdb.lookup_type(t[:-2]).pointer().pointer()
                    )
                )
            elif t.endswith("*"):
                return GdbValue(
                    super(GdbValue, self).cast(gdb.lookup_type(t[:-1]).pointer())
                )
            else:
                return GdbValue(super(GdbValue, self).cast(gdb.lookup_type(t)))
        else:
            return None

    def dereference(self):
        return GdbValue(super(GdbValue, self).dereference())

    def reference(self):
        return self.address

    @staticmethod
    def parse(s, ignore_error=False):
        # print(f"parse {s}")
        try:
            if isinstance(s, str):
                return GdbValue(gdb.parse_and_eval(s))
            else:
                return GdbValue(gdb.parse_and_eval(str(s)))
        except:
            if not ignore_error:
                print("error: %s not exists" % str(s))
                traceback.print_exc()
            return None

    @staticmethod
    def get(s, ignore_error=False):
        return GdbValue.parse(s, ignore_error)


@GdbCommandRegistry
class wq(gdb.Command):
    def __init__(self):
        super().__init__("wq", gdb.COMMAND_USER, gdb.COMPLETE_NONE, True)


class wq_generic_list:
    """
    wuqi generic list
    """

    def __init__(self, _list, cast_type_str: str):
        self.cast_type = cast_type_str
        self.head_node = _list

    def __iter__(self):
        index = 0
        curr_node = self.head_node.next
        while True:
            # print(
            #     f"__iter__ {index} 0x{int(curr_node):08X} head:0x{int(self.head_node.address):08X}"
            # )
            if int(curr_node) == int(self.head_node.address):
                break
            data = curr_node.cast(self.cast_type)
            yield data.dereference()
            curr_node = curr_node.next

            index += 1
            if index > 256:  # limit list count
                print(f"list stop foreach")
                break


class FreeRtosList:
    """Enumerator for an freertos list (ListItem_t)

    :param list_: List to enumerate
    :param cast_type_str: Type name to cast list items as
    :param check_length: If True check uxNumberOfItems to stop iteration. By default check for reaching xListEnd.
    """

    def __init__(self, list_, cast_type_str, check_length: bool = False):
        self.cast_type = gdb.lookup_type(cast_type_str).pointer()
        self.end_marker = list_["xListEnd"]
        self.head = self.end_marker["pxNext"]  # ptr to start item
        self._length = list_["uxNumberOfItems"]
        self.check_length = check_length

    @property
    def length(self):
        return self._length

    def __getitem__(self, idx):
        for i, item in enumerate(self):
            if i == idx:
                return item
        return None

    def __iter__(self):
        curr_node = self.head
        index = 0
        while True:
            if curr_node == self.end_marker.address:
                break
            if self.check_length and index >= self._length:
                break
            tmp_node = curr_node.dereference()
            data = tmp_node["pvOwner"].cast(self.cast_type)
            yield data
            index += 1
            curr_node = tmp_node["pxNext"]


def xTaskGetTickCount() -> int:
    return int(GdbValue.get("xTickCount"))


def wq_rtc_to_ms(rtc: int) -> float:
    return float(rtc / 31.25)


def get_heap_size():
    tatol_size = 0
    free = 0
    lowest = 0
    if GdbValue.get("g_multi_heap_list", True):
        g_multi_heap_list = GdbValue.get("g_multi_heap_list")
        for heap in g_multi_heap_list:
            if heap.end > heap.start and heap.heap != 0x0:
                tatol_size += heap.end - heap.start
                free += heap.heap.free_bytes
                lowest += heap.heap.minimum_free_bytes
    else:
        tatol_size = int(GdbValue.get("heap_tatol_size"))
        free = int(GdbValue.get("xFreeBytesRemaining"))
        lowest = int(GdbValue.get("xMinimumEverFreeBytesRemaining"))
    return tatol_size, free, lowest


def prvListTasksHandlerWithinSingleList(task_list):
    tcb_list = []
    num = int(task_list.uxNumberOfItems)
    index = task_list.pxIndex
    # print(task_list)
    for i in range(num):
        # print(
        #     f"num:{num} idx:{i} pxIndex:0x{int(index):X} xListEnd:0x{int(task_list.xListEnd.reference()):X}"
        # )
        if index == task_list.xListEnd.reference():
            index = index.pxNext
        if index == 0:
            break
        tcb = index.pvOwner.cast("TCB_t*")
        index = index.pxNext
        if tcb == 0:
            continue
        # print(tcb)
        tcb_list.append(tcb)
    return tcb_list


def get_task_dict():
    tcb_dict = {}

    pxReadyTasksLists = GdbValue.get("pxReadyTasksLists")
    tcb_dict["Ready"] = []
    for i, taskList in enumerate(pxReadyTasksLists):
        # print(f"pxReadyTasksLists[{i}] = {taskList}")
        tcb_dict["Ready"] += prvListTasksHandlerWithinSingleList(taskList)

    xSuspendedTaskList = GdbValue.get("xSuspendedTaskList")
    # print(f"xSuspendedTaskList = {xSuspendedTaskList}")
    tcb_dict["Suspended"] = prvListTasksHandlerWithinSingleList(xSuspendedTaskList)

    pxOverflowDelayedTaskList = GdbValue.get("pxOverflowDelayedTaskList")
    # print(f"pxOverflowDelayedTaskList = {pxOverflowDelayedTaskList}")
    tcb_dict["OverflowDelayed"] = prvListTasksHandlerWithinSingleList(
        pxOverflowDelayedTaskList
    )

    xDelayedTaskList1 = GdbValue.get("xDelayedTaskList1")
    # print(f"xDelayedTaskList1 = {xDelayedTaskList1}")
    tcb_dict["Delayed1"] = prvListTasksHandlerWithinSingleList(xDelayedTaskList1)

    xDelayedTaskList2 = GdbValue.get("xDelayedTaskList2")
    # print(f"xDelayedTaskList2 = {xDelayedTaskList2}")
    tcb_dict["Delayed2"] = prvListTasksHandlerWithinSingleList(xDelayedTaskList2)

    xTasksWaitingTermination = GdbValue.get("xTasksWaitingTermination")
    # print(f"xTasksWaitingTermination = {xTasksWaitingTermination}")
    tcb_dict["WaitingTermination"] = prvListTasksHandlerWithinSingleList(
        xTasksWaitingTermination
    )

    return tcb_dict


def get_task_list():
    tcb_list = []

    for _, taskList in get_task_dict().items():
        tcb_list += taskList

    return tcb_list
