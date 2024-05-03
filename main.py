import tkinter as tk
from skimage import data, img_as_ubyte
from PIL import Image, ImageTk

# Assuming WINDOW_WIDTH and WINDOW_HEIGHT are defined in constants.py
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW

window = tk.Tk()
window.title("CT machine")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)
window.configure(bg="gray")
window.attributes("-alpha", 0.95)

label_text = "Computed Tomography Scanner"
label = tk.Label(window, text=label_text, font=("Courier", 24), bg="gray", fg="white")
label.grid(padx=10, pady=10, row=0, column=0, columnspan=11)  # Adjust columnspan to 11

set_button_text = "SET"
set_button = tk.Button(window, text=set_button_text, font=("Courier", 16, "bold"), bg="white", fg="blue", width=20, height=2, highlightbackground="gray")
set_button.grid(padx=5, pady=10, row=2, column=0, columnspan=2)

run_button_text = "RUN"
run_button = tk.Button(window, text=run_button_text, font=("Courier", 16, "bold"), bg="white", fg="green", width=20, height=2, highlightbackground="gray")
run_button.grid(padx=5, pady=10, row=4, column=0, columnspan=2)

stop_button_text = "STOP"
stop_button = tk.Button(window, text=stop_button_text, font=("Courier", 16, "bold"), bg="white", fg="red", width=20, height=2, highlightbackground="gray")
stop_button.grid(padx=5, pady=10, row=6, column=0, columnspan=2)

continue_button_text = "CONTINUE"
continue_button = tk.Button(window, text=continue_button_text, font=("Courier", 16, "bold"), bg="white", fg=YELLOW, width=20, height=2, highlightbackground="gray")
continue_button.grid(padx=5, pady=10, row=8, column=0, columnspan=2)

log_text = tk.Text(window, font=("Courier", 16, "bold"), bg="black", fg="yellow", width=22, height=15, highlightbackground="gray")
log_text.grid(padx=5, pady=10, row=9, column=0, columnspan=2)

# Adjust column weights to make them fill the space horizontally
window.grid_columnconfigure(2, weight=1)  # Adjust column 2 weight
for col in range(9):  # Adjust weights for columns 2 through 10
    window.grid_columnconfigure(col+2, weight=1)

# Create canvas
canvas = tk.Canvas(window, bg="white", borderwidth=0, highlightbackground="gray")
canvas.grid(padx=5, pady=10, row=1, column=2, rowspan=9, columnspan=9, sticky="nsew")

# Force update to get the correct canvas dimensions
window.update_idletasks()

# Get canvas dimensions
canvas_width = canvas.winfo_width()
canvas_height = canvas.winfo_height()

# Get canvas center
canvas_cx = canvas_width // 2
canvas_cy = canvas_height // 2

# Set rectangle dimensions
rectangle_width = 500
recngle_height = 500

# Get the rectangle position
x1 = canvas_cx - rectangle_width // 2
y1 = canvas_cy - recngle_height // 2
x2 = canvas_cx + rectangle_width // 2
y2 = canvas_cy + recngle_height // 2

# Place the rectangle
canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

# Get the dummy-phantom
dummy_image = data.shepp_logan_phantom()
dummy_image = img_as_ubyte(dummy_image)  # Convert image to 8-bit for display
dummy_image = Image.fromarray(dummy_image)  # Convert numpy array to PIL Image
dummy_image = ImageTk.PhotoImage(dummy_image)  # Convert PIL Image to tkinter-compatible image

dummy_width = dummy_image.width()
dummy_height = dummy_image.height()

# Get the dumyy position
x1_dummy = canvas_cx - dummy_width // 2
y1_dummy = canvas_cy - dummy_height // 2

# Place the dummy
canvas.create_image(x1_dummy, y1_dummy, anchor="nw", image=dummy_image)

window.mainloop()

