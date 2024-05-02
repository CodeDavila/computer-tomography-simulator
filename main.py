import tkinter as tk
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

window = tk.Tk()
window.title("CT machine")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)
window.configure(bg="black")
window.attributes("-alpha", 0.90)

# CODE


window.mainloop()
