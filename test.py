import time
import os
import sys
import shutil
import win32com.client
import ctypes
import ctypes.wintypes

from win10toast import ToastNotifier


def notify(user_name):
    while True:
        time.sleep(5)
        toaster.show_toast(f"Hej {user_name}",
                           "Upp och sträck på dig!",
                           duration=10)

        while toaster.notification_active(): time.sleep(0.1)


def add_to_startup():
    # Get the path to the executable
    executable_path = os.path.abspath(sys.argv[0])

    # Get the path to the Startup folder
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Path to the shortcut
    shortcut_path = os.path.join(startup_folder, 'MyProgramName.lnk')

    # Create a shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = executable_path
    shortcut.WorkingDirectory = os.path.dirname(executable_path)
    shortcut.save()


def get_user_full_name():
    try:
        # Initialize the required structs
        UNLEN = 256
        EXTENDED_NAME_FORMAT = 3  # NameDisplay

        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        GetUserNameEx.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong)]

        # Create buffer
        size = ctypes.wintypes.DWORD(UNLEN + 1)
        name_buffer = ctypes.create_unicode_buffer(size.value)

        # Retrieve the full name
        if GetUserNameEx(EXTENDED_NAME_FORMAT, name_buffer, ctypes.byref(size)):
            return name_buffer.value
        else:
            username = os.getlogin()
            return username

    except Exception:
        username = os.getlogin()
        return username


if __name__ == "__main__":
    toaster = ToastNotifier()
    add_to_startup()
    user_name = get_user_full_name()
    notify(user_name)