import tkinter as tk
from tkinter import ttk

# GLOBAL VARIABLES

GLOBAL_FONT = "Segoe UI"
GLOBAL_FONT_SIZE = 20

# Configure Window

window = tk.Tk()

window.title("Todo Be")
window.state('zoomed')  # Start maximized
window.minsize(800,600)  # Minumum width and height

# Configure style

style = ttk.Style()

# Basically a seperate styling for button because buttons don't work well in ttk
BTN = {
    "primary": {
        "bg": "#A0D683",
        "fg": "white"
    }
}

window.mainloop()