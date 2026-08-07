import tkinter as tk

# Colours and settings (constants - set once, use everywhere)
WHITE = "#FFFFFF"   # window background
INK   = "#26313F"   # main dark text
FONT  = "Segoe UI"  # the font used everywhere

root = tk.Tk()
root.title("Emergency Q - Version 1")
root.geometry("420x700")
root.configure(bg=WHITE)

# Title heading at the top of the window
title = tk.Label(root, text="Emergency Q Prototype",
                 bg=WHITE, fg=INK, font=(FONT, 16, "bold"))
title.pack(pady=(18, 14))

root.mainloop()