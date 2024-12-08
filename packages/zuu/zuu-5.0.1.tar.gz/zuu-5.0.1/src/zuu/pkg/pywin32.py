import win32process
import pygetwindow as gw

def get_pid_from_hwnd(hwnd):
    """
    Get the process ID given the handle of a window.

    Args:
        hwnd (int or gw.Win32Window): The handle of the window. If it is an instance of gw.Win32Window, its handle will be extracted.

    Returns:
        int or None: The process ID of the window, or None if an error occurred.
    """
    if not isinstance(hwnd, int):
        assert isinstance(hwnd, gw.Win32Window)
        hwnd = hwnd._hWnd

    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        print(f"Error: {e}")
        return None