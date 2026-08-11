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

# --- Search box ---
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, font=(FONT, 11),
                        bg="#F1F4F8", fg=INK, relief="flat")
search_entry.pack(fill="x", padx=20, pady=(0, 6), ipady=6)

# Frame that will hold the list of hospitals
list_frame = tk.Frame(root, bg=WHITE)
list_frame.pack(fill="x", padx=20, pady=(10, 0))

# Show each hospital as a row in the list, optionally filtered by a search query
def update_list(query=""):
    # Remove the old rows before rebuilding. Without this, every keystroke would stack a new copy of the list underneath the old one.
    for widget in list_frame.winfo_children():
        widget.destroy()

    #Lowercasing both sides makes the search case-insensitive, and "in" on strings is a substring check, so "shore" matches "North Shore Hospital" even though it's not at the start.
    query = query.lower()
    matches = [h for h in HOSPITALS if query in h["name"].lower()]

    if len(matches) == 0:
        empty = tk.Label(list_frame, text="No hospitals found",
                         bg=WHITE, fg="#8A94A6", font=(FONT, 10, "italic"))
        empty.pack(pady=20)
        return

    for h in matches:
        row = tk.Frame(list_frame, bg=WHITE) #This frame exists purely as a container that defines a horizontal strip
        row.pack(fill="x", pady=1) # Stretches the frame horizontally to fill all available width in its parent
        label = tk.Label(row, text=h["name"] + " (" + h["type"] + ")",
                         bg=WHITE, fg=INK, font=(FONT, 10), anchor="w")
        label.pack(side="left", padx=10, pady=6)
        dot = tk.Label(row, text="●", bg=WHITE, fg=wait_colour(h["wait"]), font=(FONT, 11))
        dot.pack(side="right", padx=10)
        row.bind("<Button-1>", lambda event, hosp=h, r=row: select_row(hosp, r))
        label.bind("<Button-1>", lambda event, hosp=h, r=row: select_row(hosp, r))

# Re-filter the list every time the search text changes
def on_search(*args):
    update_list(search_var.get())

search_var.trace_add("write", on_search)

# --- Details panel (shows the selected hospital) ---
details_frame = tk.Frame(root, bg="#F1F4F8")
details_frame.pack(fill="x", side="bottom", padx=20, pady=20)

details_name = tk.Label(details_frame, text="Select a hospital",
                        bg="#F1F4F8", fg=INK, font=(FONT, 12, "bold"))
details_name.pack(anchor="w", padx=12, pady=(12, 2))

details_info = tk.Label(details_frame, text="",
                        bg="#F1F4F8", fg=INK, font=(FONT, 10), justify="left")
details_info.pack(anchor="w", padx=12, pady=(0, 12))

# Fill the details panel with one hospital's information
def show_details(hospital):
    details_name.config(text=hospital["name"])
    details_info.config(text="Wait: " + str(hospital["wait"]) + " min\n"
                             + "Phone: " + hospital["phone"] + "\n"
                             + "Type: " + hospital["type"])

# Remember which row frame is currently highlighted
selected_row = None

# Highlight the clicked row and show its details
def select_row(hospital, row):
    global selected_row
    if selected_row is not None:
        selected_row.config(bg=WHITE)
    row.config(bg="#DCE6F5")
    selected_row = row
    show_details(hospital)

# Show the full list at startup
update_list()

root.mainloop()