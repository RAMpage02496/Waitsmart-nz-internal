import tkinter as tk

# Colours and settings (constants - set once, use everywhere)
WHITE = "#FFFFFF"   # window background
INK   = "#26313F"   # main dark text
FONT  = "Segoe UI"  # the font used everywhere
GREEN = "#00A152"   # short wait
AMBER = "#E08E00"   # medium wait
RED   = "#E03A2F"   # long wait

SHORT  = 30   # under this many minutes = green
MEDIUM = 90   # under this many minutes = amber; otherwise red

root = tk.Tk()

# Hospital data - a list of dictionaries (one dictionary per hospital)
HOSPITALS = [
    {"name": "Auckland City Hospital",       "wait": 45,  "phone": "09 367 0000", "type": "Public"},
    {"name": "Middlemore Hospital",          "wait": 120, "phone": "09 276 0000", "type": "Public"},
    {"name": "North Shore Hospital",         "wait": 30,  "phone": "09 486 8900", "type": "Public"},
    {"name": "Waitakere Hospital",           "wait": 80,  "phone": "09 839 0000", "type": "Public"},
    {"name": "Starship Children's Hospital", "wait": 15,  "phone": "09 367 0000", "type": "Public"},
    {"name": "Greenlane Clinical Centre",    "wait": 10,  "phone": "09 638 9909", "type": "Public"},
    {"name": "Southern Cross Hospital",      "wait": 5,   "phone": "09 623 8900", "type": "Private"},
    {"name": "Mercy Hospital Auckland",      "wait": 15,  "phone": "09 623 3456", "type": "Private"},
]

root.title("Emergency Q - Version 1")
root.geometry("420x700")
root.configure(bg=WHITE)

# Decide the status colour for a wait time (in minutes)
def wait_colour(minutes):
    if minutes < SHORT:   # under 30 = green; exactly 30 = amber
        return GREEN
    elif minutes < MEDIUM:
        return AMBER
    else:
        return RED

# Title heading at the top of the window
title = tk.Label(root, text="Emergency Q Prototype",
                 bg=WHITE, fg=INK, font=(FONT, 16, "bold"))
title.pack(pady=(18, 14))

# Frame that will hold the list of hospitals
list_frame = tk.Frame(root, bg=WHITE)
list_frame.pack(fill="x", padx=20, pady=(10, 0))

# Show each hospital as a row in the list
for h in HOSPITALS:
    row = tk.Frame(list_frame, bg=WHITE)
    row.pack(fill="x", pady=1)
    label = tk.Label(row, text=h["name"] + " (" + h["type"] + ")",
                     bg=WHITE, fg=INK, font=(FONT, 10), anchor="w")
    label.pack(side="left", padx=10, pady=6)
    dot = tk.Label(row, text="●", bg=WHITE, fg=wait_colour(h["wait"]), font=(FONT, 11))
    dot.pack(side="right", padx=10)

root.mainloop()