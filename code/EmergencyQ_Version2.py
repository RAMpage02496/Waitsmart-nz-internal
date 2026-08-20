"""
Emergency Q - Version 2
"""

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

# A single hospital. Using a class instead of a dictionary means each hospital carries its own data and its own behaviour, like status_colour().
class Hospital:
    def __init__(self, name, wait, phone, kind):
        self.name = name
        self.wait = wait
        self.phone = phone
        self.kind = kind          # "Public" or "Private"

    # Work out this hospital's status colour from its own wait time
    def status_colour(self):
        if self.wait < SHORT:
            return GREEN
        elif self.wait < MEDIUM:
            return AMBER
        else:
            return RED

# Read the data file and turn each line into a Hospital object, robust building so a missing file or a bad line won't crash the program (try and except, and skip bad lines).
def load_hospitals(filename):
    hospitals = []

    try:
        file = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Could not find the data file:", filename)
        return hospitals          # return an empty list so the app still opens

    for line in file:
        line = line.strip()
        if line == "":
            continue

        parts = line.split(",")
        if len(parts) != 4:                       # every line must have all 4 fields
            print("Skipping bad line (need 4 fields):", line)
            continue

        try:
            wait = int(parts[1])
        except ValueError:                        # the wait time wasn't a number
            print("Skipping line with a bad wait time:", line)
            continue

        hospitals.append(Hospital(parts[0], wait, parts[2], parts[3]))

    file.close()
    return hospitals


root = tk.Tk()

# Hospital data - now loaded from the file instead of hard-coded into the main code
HOSPITALS = load_hospitals("hospitals.txt")


root.title("Emergency Q - Version 1")
root.geometry("420x700")
root.configure(bg=WHITE)

# Title heading at the top of the window
title = tk.Label(root, text="Emergency Q Prototype",
                 bg=WHITE, fg=INK, font=(FONT, 16, "bold"))
title.pack(pady=(18, 14))

# Search box
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, font=(FONT, 11),
                        bg="#F1F4F8", fg=INK, relief="flat")
search_entry.pack(fill="x", padx=20, pady=(0, 6), ipady=6)

# Frame that will hold the list of hospitals
list_frame = tk.Frame(root, bg=WHITE)
list_frame.pack(fill="x", padx=20, pady=(10, 0))

# Result count
count_label = tk.Label(root, text="", bg=WHITE, fg="#6B7686", font=(FONT, 9, "italic"))
count_label.pack(anchor="w", padx=22, pady=(6, 2))

# Colour legend (what the dots mean)
legend = tk.Frame(root, bg=WHITE)
legend.pack(fill="x", padx=20, pady=(4, 0))
for text, colour in [("Short wait", GREEN), ("Medium", AMBER), ("Long wait", RED)]:
    tk.Label(legend, text="● " + text, bg=WHITE, fg=colour, font=(FONT, 9)).pack(side="left", padx=(0, 12))

# Show each hospital as a row in the list, optionally filtered by a search query
def update_list(query=""):
    global selected_row
    selected_row = None
    # Remove the old rows before rebuilding. Without this, every keystroke would stack a new copy of the list underneath the old one.
    for widget in list_frame.winfo_children():
        widget.destroy()

    #Lowercasing both sides makes the search case-insensitive, and "in" on strings is a substring check, so "shore" matches "North Shore Hospital" even though it's not at the start.
    query = query.lower()
    matches = [h for h in HOSPITALS if query in h.name.lower()]
    count_label.config(text="Showing " + str(len(matches)) + " hospitals")

    if len(matches) == 0:
        empty = tk.Label(list_frame, text="No hospitals found",
                         bg=WHITE, fg="#8A94A6", font=(FONT, 10, "italic"))
        empty.pack(pady=20)
        return

    for h in matches:
        row = tk.Frame(list_frame, bg=WHITE) #This frame exists purely as a container that defines a horizontal strip
        row.pack(fill="x", pady=1) # Stretches the frame horizontally to fill all available width in its parent
        label = tk.Label(row, text=h.name + " (" + h.kind + ")",
                         bg=WHITE, fg=INK, font=(FONT, 10), anchor="w")
        label.pack(side="left", padx=10, pady=6)
        dot = tk.Label(row, text="●", bg=WHITE, fg=h.status_colour(), font=(FONT, 11))
        dot.pack(side="right", padx=10)
        wait_lbl = tk.Label(row, text=str(h.wait) + " min",
                            bg=WHITE, fg="#6B7686", font=(FONT, 9))
        wait_lbl.pack(side="right", padx=(0, 4))
        row.bind("<Button-1>", lambda event, hosp=h, r=row: select_row(hosp, r))
        label.bind("<Button-1>", lambda event, hosp=h, r=row: select_row(hosp, r))

# Re-filter the list every time the search text changes
def on_search(*args):
    update_list(search_var.get())

search_var.trace_add("write", on_search)

# Details panel (shows the selected hospital)
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
    details_name.config(text=hospital.name)
    details_info.config(text="Wait: " + str(hospital.wait) + " min\n"
                             + "Phone: " + hospital.phone + "\n"
                             + "Type: " + hospital.kind)

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