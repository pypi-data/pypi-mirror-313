import win32process
import win32gui
import win32con
import win32api
import winxpgui
import pywintypes
from functools import partial
from ctypes import windll, c_ulong, byref, create_string_buffer

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi


def close_handle(handle):
    kernel32.CloseHandle(handle)


def get_wnd_fg():
    return user32.GetForegroundWindow()


def get_wnd_focus():
    try:
        wnd = user32.GetForegroundWindow()
        tid_self = win32api.GetCurrentThreadId()
        tid, pid = win32process.GetWindowThreadProcessId(wnd)
        if tid != tid_self:
            win32process.AttachThreadInput(tid, tid_self, True)
            hwnd = win32gui.GetFocus()
            win32process.AttachThreadInput(tid, tid_self, False)
            return hwnd
        return win32gui.GetFocus()
    except pywintypes.error:
        return 0


def get_wnd_top_list():
    def enum(wnd, _):
        if not win32gui.GetParent(wnd) and win32gui.IsWindowVisible(wnd) and win32gui.GetWindowText(wnd):
            top_list.append(wnd)

    top_list = []
    win32gui.EnumWindows(enum, None)
    return top_list


def enum_wnd(cb):
    def enum(wnd, _):
        nonlocal end
        if not end:
            end = cb(wnd)
            if not end:
                win32gui.EnumChildWindows(wnd, enum_child, None)

    def enum_child(wnd, _):
        nonlocal end
        if not end:
            end = cb(wnd)

    end = None
    win32gui.EnumWindows(enum, None)
    return end


def get_wnd_rect(wnd):
    ratio_x, ratio_y = 1, 1
    left, top, right, bottom = win32gui.GetWindowRect(wnd)
    width = int((right - left) * ratio_x)
    height = int((bottom - top) * ratio_y)
    return left, top, width, height


def get_wnd_title(wnd):
    text = win32gui.GetWindowText(wnd)
    if text:
        return text
    else:
        buf = win32gui.PyMakeBuffer(255)
        length = win32gui.SendMessage(wnd, win32con.WM_GETTEXT, 255, buf)
        result = buf.tobytes()[:length * 2:2]
        try:
            return result.decode("utf-8")
        except UnicodeDecodeError:
            return ''


def query_wnd(query, limit=None):
    """
    :param query: {'parent': {...query}, index: None, caption:None, class:None}
    :param limit: set(), pick from limit if limit is not empty
    :return: None,set(),int->wnd
    """

    def cb_caption(caption_, limit_, wnd_):
        if get_wnd_title(wnd_) == caption_:
            if not limit_ or wnd_ in limit_:
                result.add(wnd_)

    def cb_cls(cls_, limit_, wnd_):
        if win32gui.GetClassName(wnd_) == cls_:
            if not limit_ or wnd_ in limit_:
                result.add(wnd_)

    def get_children(wnd__):
        def enum_child(wnd_, _):
            s.append(wnd_)

        s = []
        win32gui.EnumChildWindows(wnd__, enum_child, None)
        return s

    if not limit:
        limit = set()
    if isinstance(query, str):
        query = {'caption': query}
    result = set()
    caption = query.get('caption')
    if caption:
        limit = set(limit)
        result = set()
        enum_wnd(partial(cb_caption, caption, limit))
        limit = result
    cls = query.get('cls')
    if cls:
        limit = set(limit)
        result = set()
        enum_wnd(partial(cb_cls, cls, limit))
        limit = result
    parent = query.get('parent')
    index = query.get('index')
    if parent:
        limit = set(limit)
        result = set()
        ps = query_wnd(parent)
        if not ps:
            return None
        elif isinstance(ps, set):
            for p in ps:
                children = get_children(p)
                if index is None:
                    if wnd in children:
                        if not limit or wnd in limit:
                            result.add(wnd)
                else:
                    try:
                        wnd = children[index]
                    except IndexError:
                        wnd = None
                    if wnd:
                        if not limit or wnd in limit:
                            result.add(wnd)
    return list(result)


def set_wnd_transparent(hwnd, alpha=0.5):
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
    )
    winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), int(alpha * 255), win32con.LWA_ALPHA)


def set_wnd_top(hwnd):
    x, y, w, h = get_wnd_rect(hwnd)
    mask = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if mask & win32con.WS_EX_TOPMOST:
        value = win32con.HWND_NOTOPMOST
    else:
        value = win32con.HWND_TOPMOST
    win32gui.SetWindowPos(hwnd, value, x, y, w, h, 0)
    return value == win32con.HWND_TOPMOST


def get_proc_id_by_wnd(hwnd):
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    return pid  # pid.value is the integer value of process ID


def get_proc(pid, flags=0x400 | 0x10):
    return kernel32.OpenProcess(flags, False, pid)


def get_proc_id(handle_proc):
    return kernel32.GetProcessId(handle_proc)


def get_proc_name(handle_proc, length=512, encoding='utf-8'):
    proc_name = create_string_buffer(b'\x00' * length)
    psapi.GetModuleBaseNameA(handle_proc, None, byref(proc_name), length)
    return proc_name.value.decode(encoding)
