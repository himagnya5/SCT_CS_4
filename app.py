import tkinter as tk
from datetime import datetime
from pathlib import Path
import csv

APP_NAME = "Key Event Recorder (In-App Only)"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "key_events.csv"

LOG_DIR.mkdir(exist_ok=True)
if not LOG_FILE.exists():
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "key", "char"])

def log_key(event: tk.Event):
    # event.char is printable character (may be '' for special keys)
    char = event.char if event.char and event.char.isprintable() else ""
    key = event.keysym  # e.g., 'a', 'BackSpace', 'Shift_L', 'Return'
    ts = datetime.now().isoformat(timespec="milliseconds")
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, key, char])

def clear_log():
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["timestamp", "key", "char"])

def open_folder():
    # Opens the logs folder in the OS file explorer
    import os, subprocess, sys
    path = str(LOG_DIR.resolve())
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

root = tk.Tk()
root.title(APP_NAME)
root.geometry("720x420")

info = tk.Label(
    root,
    text=(
        "This demo records only the keys you press while this window is focused\n"
        "and saves them to logs/key_events.csv with timestamps.\n"
        "Use the text box below to type.\n"
        "Ethics: Do not record anyone's input without explicit consent."
    ),
    justify="center",
    pady=10
)
info.pack(fill="x")

# Buttons
btns = tk.Frame(root)
tk.Button(btns, text="Open logs folder", command=open_folder).pack(side="left", padx=6)
tk.Button(btns, text="Clear log", command=clear_log).pack(side="left", padx=6)
tk.Button(btns, text="Quit", command=root.destroy).pack(side="left", padx=6)
btns.pack(pady=6)

# Text area for typing
text = tk.Text(root, height=12)
text.pack(fill="both", expand=True, padx=10, pady=10)
text.focus_set()

# Bind keypress handler to the whole window (only when focused)
root.bind("<KeyPress>", log_key)

root.mainloop()
