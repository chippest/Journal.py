import keyboard
import subprocess
import os

# File to store the process id for later removal
PID_FILE = "hotkey_pid.txt"

def launch_entry1():
    # Launch entry1.py (adjust the command if needed)
    subprocess.Popen(["python", "entry1.py"])

# Register the global hotkey: Ctrl+Alt+1
keyboard.add_hotkey('ctrl+alt+1', launch_entry1)

# Write current process id to a file
with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

print("Global hotkey (Ctrl+Alt+1) registered. Press ESC to exit and remove the hotkey.")
# Keep the script running until ESC is pressed
keyboard.wait('esc')
