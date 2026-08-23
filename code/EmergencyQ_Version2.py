"""
Emergency Q - Version 2
"""

import tkinter as tk
import os   # lets us work out file paths
import random   # for the live wait-time changes
import math   # for the distance calculation

# The folder THIS .py file lives in. We build the data-file path from here so
# hospitals.txt is always found, no matter which folder the program is run from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    def __init__(self, name, wait, phone, kind, lat, lon):
        self.name = name
        self.wait = wait
        self.phone = phone
        self.kind = kind          # "Public" or "Private"
        self.lat = lat           
        self.lon = lon            

    # Work out this hospital's status colour from its own wait time
    def status_colour(self):
        if self.wait < SHORT:
            return GREEN
        elif self.wait < MEDIUM:
            return AMBER
        else:
            return RED

# Distance in km between two points on Earth, using their latitude/longitude (Haversine formula)
def distance_km(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

# Read the suburbs file into a dictionary: {suburb name: (lat, lon)}
def load_suburbs(filename):
    suburbs = {}
    try:
        file = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Could not find the suburbs file:", filename)
        return suburbs
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.split(",")
        if len(parts) != 3:
            continue
        try:
            suburbs[parts[0]] = (float(parts[1]), float(parts[2]))
        except ValueError:
            continue
    file.close()
    return suburbs

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
        if len(parts) != 6:                       # every line must have all 6 fields
            print("Skipping bad line (need 6 fields):", line)
            continue

        try:
            wait = int(parts[1])
            lat  = float(parts[4])                # coordinates are decimals, so float
            lon  = float(parts[5])                
        except ValueError:                        # the wait time wasn't a number
            print("Skipping line with a bad wait time:", line)
            continue

        hospitals.append(Hospital(parts[0], wait, parts[2], parts[3], lat, lon))

    file.close()
    return hospitals


# The whole application, wrapped in a class. Data and widgets live on self.
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Emergency Q - Version 2")
        self.root.geometry("420x700")
        self.root.configure(bg=WHITE)

        # Hospital data - loaded from the file instead of hard-coded
        self.hospitals = load_hospitals(os.path.join(BASE_DIR, "hospitals.txt"))
        self.suburbs = load_suburbs(os.path.join(BASE_DIR, "suburbs.txt"))
        self.user_location = None                        # (lat, lon) once a suburb is picked
        self.location_var = tk.StringVar(value="(choose)")
        self.selected_row = None
        self.search_var = tk.StringVar()
        self.sort_var = tk.BooleanVar()   # is "sort by shortest wait" ticked?
        self.nearest_var = tk.BooleanVar()   # is "sort by nearest" ticked?


        self.build_ui()
        self.update_list()
        self.update_times()   # start the live wait-time updates

    # Build all the widgets
    def build_ui(self):
        title = tk.Label(self.root, text="Emergency Q Prototype",
                         bg=WHITE, fg=INK, font=(FONT, 16, "bold"))
        title.pack(pady=(18, 14))

        # Search box
        search_entry = tk.Entry(self.root, textvariable=self.search_var, font=(FONT, 11),
                                bg="#F1F4F8", fg=INK, relief="flat")
        search_entry.pack(fill="x", padx=20, pady=(0, 6), ipady=6)
        self.search_var.trace_add("write", self.on_search)

        # Sort toggle
        sort_check = tk.Checkbutton(self.root, text="Sort by shortest wait first",
                                    variable=self.sort_var, command=self.on_search,
                                    bg=WHITE, fg=INK, font=(FONT, 9), activebackground=WHITE)
        sort_check.pack(anchor="w", padx=18)

        # Nearest toggle
        nearest_check = tk.Checkbutton(self.root, text="Sort by nearest first",
                                       variable=self.nearest_var, command=self.on_search,
                                       bg=WHITE, fg=INK, font=(FONT, 9), activebackground=WHITE)
        nearest_check.pack(anchor="w", padx=18)

        # Location picker
        loc_frame = tk.Frame(self.root, bg=WHITE)
        loc_frame.pack(fill="x", padx=18, pady=(2, 0))
        tk.Label(loc_frame, text="Your suburb:", bg=WHITE, fg=INK, font=(FONT, 9)).pack(side="left")
        location_menu = tk.OptionMenu(loc_frame, self.location_var,
                                      *self.suburbs.keys(), command=self.on_location)
        location_menu.pack(side="left", padx=6)

        # Frame that will hold the list of hospitals
        self.list_frame = tk.Frame(self.root, bg=WHITE)
        self.list_frame.pack(fill="x", padx=20, pady=(10, 0))

        # Result count
        self.count_label = tk.Label(self.root, text="", bg=WHITE, fg="#6B7686", font=(FONT, 9, "italic"))
        self.count_label.pack(anchor="w", padx=22, pady=(6, 2))

        # Colour legend (what the dots mean)
        legend = tk.Frame(self.root, bg=WHITE)
        legend.pack(fill="x", padx=20, pady=(4, 0))
        for text, colour in [("Short wait", GREEN), ("Medium", AMBER), ("Long wait", RED)]:
            tk.Label(legend, text="● " + text, bg=WHITE, fg=colour, font=(FONT, 9)).pack(side="left", padx=(0, 12))

        # Details panel (shows the selected hospital)
        self.details_frame = tk.Frame(self.root, bg="#F1F4F8")
        self.details_frame.pack(fill="x", side="bottom", padx=20, pady=20)

        self.details_name = tk.Label(self.details_frame, text="Select a hospital",
                                     bg="#F1F4F8", fg=INK, font=(FONT, 12, "bold"))
        self.details_name.pack(anchor="w", padx=12, pady=(12, 2))

        self.details_info = tk.Label(self.details_frame, text="",
                                     bg="#F1F4F8", fg=INK, font=(FONT, 10), justify="left")
        self.details_info.pack(anchor="w", padx=12, pady=(0, 12))

    # Show each hospital as a row in the list, optionally filtered by a search query
    def update_list(self, query=""):
        self.selected_row = None
        # Remove the old rows before rebuilding. Without this, every keystroke would stack a new copy of the list underneath the old one.
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        #Lowercasing both sides makes the search case-insensitive, and "in" on strings is a substring check, so "shore" matches "North Shore Hospital" even though it's not at the start.
        query = query.lower()
        matches = [h for h in self.hospitals if query in h.name.lower()]
        if self.sort_var.get():
            matches.sort(key=lambda h: h.wait,)
        elif self.nearest_var.get() and self.user_location is not None: # only sorts if a suburb is piced
            ulat, ulon = self.user_location
            matches.sort(key=lambda h: distance_km(ulat, ulon, h.lat, h.lon))
        self.count_label.config(text="Showing " + str(len(matches)) + " hospitals")

        if len(matches) == 0:
            empty = tk.Label(self.list_frame, text="No hospitals found",
                             bg=WHITE, fg="#8A94A6", font=(FONT, 10, "italic"))
            empty.pack(pady=20)
            return

        for h in matches:
            row = tk.Frame(self.list_frame, bg=WHITE) #This frame exists purely as a container that defines a horizontal strip
            row.pack(fill="x", pady=1) # Stretches the frame horizontally to fill all available width in its parent
            label = tk.Label(row, text=h.name + " (" + h.kind + ")",
                             bg=WHITE, fg=INK, font=(FONT, 10), anchor="w")
            label.pack(side="left", padx=10, pady=6)
            dot = tk.Label(row, text="●", bg=WHITE, fg=h.status_colour(), font=(FONT, 11))
            dot.pack(side="right", padx=10)
            wait_lbl = tk.Label(row, text=str(h.wait) + " min",
                                bg=WHITE, fg="#6B7686", font=(FONT, 9))
            wait_lbl.pack(side="right", padx=(0, 4))
            if self.user_location is not None:
                ulat, ulon = self.user_location
                km = distance_km(ulat, ulon, h.lat, h.lon)
                dist_lbl = tk.Label(row, text=str(round(km, 1)) + " km",
                                    bg=WHITE, fg="#3A7BD5", font=(FONT, 9))
                dist_lbl.pack(side="right", padx=(0, 4))
            row.bind("<Button-1>", lambda event, hosp=h, r=row: self.select_row(hosp, r))
            label.bind("<Button-1>", lambda event, hosp=h, r=row: self.select_row(hosp, r))

    # Re-filter the list every time the search text changes
    def on_search(self, *args):
        self.update_list(self.search_var.get())

    # Called when the user picks a suburb from the dropdown
    def on_location(self, choice):
        self.user_location = self.suburbs[choice]
        self.update_list(self.search_var.get())    # reraw so distances show / update

    # Fill the details panel with one hospital's information
    def show_details(self, hospital):
        self.details_name.config(text=hospital.name)
        self.details_info.config(text="Wait: " + str(hospital.wait) + " min\n"
                                      + "Phone: " + hospital.phone + "\n"
                                      + "Type: " + hospital.kind)

    # Highlight the clicked row and show its details
    def select_row(self, hospital, row):
        if self.selected_row is not None:
            self.selected_row.config(bg=WHITE)
        row.config(bg="#DCE6F5")
        self.selected_row = row
        self.show_details(hospital)

    # Every few seconds, nudge each hospital's wait a little to simulate a live feed
    def update_times(self):
        for h in self.hospitals:
            h.wait = max(0, h.wait + random.randint(-6, 6))  # never below 0, drift the wait up or down a bit
        self.update_list(self.search_var.get())          # refresh the list with the new times
        self.root.after(3000, self.update_times)         # run again in 3 seconds

    def run(self):
        self.root.mainloop()


# Make the app and start it
if __name__ == "__main__":
    app = App()
    app.run()