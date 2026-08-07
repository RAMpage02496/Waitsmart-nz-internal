import tkinter as tk

# Colours and settings (constants - set once, use everywhere)
WHITE = "#FFFFFF"   # window background
INK   = "#26313F"   # main dark text
FONT  = "Segoe UI"  # the font used everywhere

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

# Title heading at the top of the window
title = tk.Label(root, text="Emergency Q Prototype",
                 bg=WHITE, fg=INK, font=(FONT, 16, "bold"))
title.pack(pady=(18, 14))

root.mainloop()