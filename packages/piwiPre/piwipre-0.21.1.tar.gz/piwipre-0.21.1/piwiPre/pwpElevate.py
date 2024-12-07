# ===============================================
# Disclaimer:
# This code is a pure copy of elevate-0.1.3
# as found on https://pypi.org/project/elevate
# and maintained by barney.gale@gmail.com
#
# copied here because elevate refuses to install on my PyCharm setup, with strange windows error
#
# patch: execute the SAME python interpreter with the same cmdline arguments
#        so rely on orig_argv rather than argv
#
# patch: add --user username, to remember who was the user
#
# ===============================================

import sys
import subprocess
import getpass
import ctypes
from ctypes import POINTER, c_ulong, c_char_p, c_int, c_void_p
from ctypes.wintypes import HANDLE, BOOL, DWORD, HWND, HINSTANCE, HKEY
from ctypes import windll

# Constant definitions

SEE_MASK_NOCLOSEPROCESS = 0x00000040        # noqa
SEE_MASK_NO_CONSOLE = 0x00008000

# Type definitions

PHANDLE = ctypes.POINTER(HANDLE)           # noqa
PDWORD = ctypes.POINTER(DWORD)             # noqa


class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize',       DWORD),
        ('fMask',        c_ulong),
        ('hwnd',         HWND),
        ('lpVerb',       c_char_p),
        ('lpFile',       c_char_p),
        ('lpParameters', c_char_p),
        ('lpDirectory',  c_char_p),
        ('nShow',        c_int),
        ('hInstApp',     HINSTANCE),
        ('lpIDList',     c_void_p),
        ('lpClass',      c_char_p),
        ('hKeyClass',    HKEY),
        ('dwHotKey',     DWORD),
        ('hIcon',        HANDLE),
        ('hProcess',     HANDLE)]

    def __init__(self, **kw):
        super(ShellExecuteInfo, self).__init__()
        self.cbSize = ctypes.sizeof(self)
        for field_name, field_value in kw.items():
            setattr(self, field_name, field_value)


PShellExecuteInfo = POINTER(ShellExecuteInfo)


# Function definitions

ShellExecuteEx = windll.shell32.ShellExecuteExA
ShellExecuteEx.argtypes = (PShellExecuteInfo, )                  # noqa
ShellExecuteEx.restype = BOOL

WaitForSingleObject = windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = (HANDLE, DWORD)                   # noqa
WaitForSingleObject.restype = DWORD

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = (HANDLE, )                                # noqa
CloseHandle.restype = BOOL


# At last, the actual implementation!

def elevate(show_console=True):
    if windll.shell32.IsUserAnAdmin():
        return
    else:  # pragma: no cover: requires user interaction with system UI, which is not easy in automated tests
        username = getpass.getuser()
        args = sys.orig_argv or sys.argv
        params = ShellExecuteInfo(
            fMask=SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE,
            hwnd=None,
            lpVerb=b'runas',
            lpFile=args[0].encode('cp1252'),  # lpFile=sys.executable.encode('cp1252'),
            lpParameters=subprocess.list2cmdline(args[1:]+['--user', username]).encode('cp1252'),
            nShow=int(show_console))
        try:
            if not ShellExecuteEx(ctypes.byref(params)):
                raise ctypes.WinError()
        except OSError as e:
            print(f"OS Error {e}")
        handle = params.hProcess

        ret = DWORD()
        WaitForSingleObject(handle, -1)
        if windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(ret)) == 0:
            raise ctypes.WinError()
        CloseHandle(handle)
        sys.exit(ret.value)
