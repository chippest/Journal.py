import ctypes
import ctypes.wintypes
import subprocess
import sys

# Define constants
HOTKEY_ID = 1
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
VK_1 = 0x31
WM_HOTKEY = 0x0312

# Load user32.dll
user32 = ctypes.windll.user32

def register_hotkey():
    # Register the hotkey: Ctrl+Alt+1
    if not user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL | MOD_ALT, VK_1):
        print("Unable to register hotkey. It might already be in use.")
        sys.exit(1)

def unregister_hotkey():
    user32.UnregisterHotKey(None, HOTKEY_ID)

def message_loop():
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
            # Execute the Python script using pythonw.exe to avoid opening a console window.
            subprocess.Popen(
                [r"C:\Windows\pyw.exe", r"C:\Users\Dell\Documents\Python\scripts\entry1.py"],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageA(ctypes.byref(msg))

def main():
    register_hotkey()
    try:
        print("Hotkey Ctrl+Alt+1 registered. Press the key combination to run your Python script.")
        print("Press Ctrl+C to exit.")
        message_loop()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        unregister_hotkey()

if __name__ == '__main__':
    main()
