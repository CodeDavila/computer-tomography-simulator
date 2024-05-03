import tkinter as tk
from skimage import data, img_as_ubyte
from PIL import Image, ImageTk
import numpy as np
from skimage.transform import resize  # Import resize function from skimage.transform

# Assuming WINDOW_WIDTH and WINDOW_HEIGHT are defined in constants.py
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW

# Create the main window
window = tk.Tk()
window.title("CT machine")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)
window.configure(bg="gray")
window.attributes("-alpha", 0.95)  # Set window transparency

# Add label for the CT scanner title
label_text = "Computed Tomography Scanner"
label = tk.Label(window, text=label_text, font=("Courier", 24), bg="gray", fg="white")
label.grid(padx=10, pady=10, row=0, column=0, columnspan=11)  # Adjust columnspan to 11

# Add buttons for setting parameters, running, stopping, and continuing the CT scan
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

# Add a text widget for logging
log_text = tk.Text(window, font=("Courier", 16, "bold"), bg="black", fg="yellow", width=22, height=15, highlightbackground="gray")
log_text.grid(padx=5, pady=10, row=9, column=0, columnspan=2)

# Adjust column weights to make them fill the space horizontally
window.grid_columnconfigure(2, weight=1)  # Adjust column 2 weight
for col in range(9):  # Adjust weights for columns 2 through 10
    window.grid_columnconfigure(col+2, weight=1)

# Create canvas for displaying images
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

# Set rectangle dimensions for visualization purposes
rectangle_width = 500
rectangle_height = 500

# Get the rectangle position
x1 = canvas_cx - rectangle_width // 2
y1 = canvas_cy - rectangle_height // 2
x2 = canvas_cx + rectangle_width // 2
y2 = canvas_cy + rectangle_height // 2

# Place the rectangle on the canvas
canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

# Get the dummy-phantom image
dummy = data.shepp_logan_phantom()

# Resize the dummy phantom to fit the canvas properly
dummy = resize(dummy, (350, 350), anti_aliasing=True)

# Convert image to 8-bit for display
dummy_image = img_as_ubyte(dummy)

# Convert numpy array to PIL Image
dummy_image = Image.fromarray(dummy_image)

# Convert PIL Image to tkinter-compatible image
dummy_image = ImageTk.PhotoImage(dummy_image)

# Get the dimensions of the dummy image
dummy_width = dummy_image.width()
dummy_height = dummy_image.height()

# Get the position to place the dummy image on the canvas
x1_dummy = canvas_cx - dummy_width // 2
y1_dummy = canvas_cy - dummy_height // 2

# Place the dummy image on the canvas
canvas.create_image(x1_dummy, y1_dummy, anchor="nw", image=dummy_image)

# Place the dummy in the camera
diagonal = np.sqrt(dummy_height ** 2 + dummy_width ** 2)
camera_height = int(np.ceil(diagonal - dummy_height) + 2)
camera_width = int(np.ceil(diagonal - dummy_width) + 2)
camera = np.zeros((dummy_height + camera_height, dummy_width + camera_width))
camera[
    int(np.ceil(camera_height / 2)) : (int(np.ceil(camera_height / 2)) + dummy_height),
    int(np.ceil(camera_width / 2)) : (int(np.ceil(camera_width / 2)) + dummy_width),
] = dummy

camera_image = img_as_ubyte(camera)
camera_image = Image.fromarray(camera_image)
camera_image = ImageTk.PhotoImage(camera_image)

camera_width = camera_image.width()
camera_height = camera_image.height()

x1_camera = canvas_cx - camera_width // 2
y1_camera = canvas_cy - camera_height //2

## TODO: Transicion ANIMATE from canvas.create_image(*args: x1_dummy, *args: y1_dummy, anchor="nw", image=dummy_image) to this
canvas.create_image(x1_camera, y1_camera, anchor="nw", image=camera_image)

window.mainloop()
