import tkinter as tk  # Import tkinter module
from skimage import data # Import necessary functions from skimage module
from skimage.util import img_as_ubyte
from PIL import Image, ImageTk  # Import necessary classes from PIL module
import numpy as np  # Import numpy module
from skimage.transform import resize  # Import resize function from skimage.transform
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW  # Import constants
from scipy.ndimage import rotate

# Create the main window
window = tk.Tk()  # Initialize tkinter window
window.title("CT machine")  # Set window title
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # Set window size
window.resizable(False, False)  # Disable window resizing
window.configure(bg="gray")  # Set window background color
window.attributes("-alpha", 0.95)  # Set window transparency

# Add label for the CT scanner title
label_text = "Computed Tomography Scanner"  # Define label text
label = tk.Label(window, text=label_text, font=("Courier", 24), bg="gray", fg="white")  # Create label widget
label.grid(padx=10, pady=10, row=0, column=0, columnspan=11)  # Place label in the window

# Add buttons for setting parameters, running, stopping, and continuing the CT scan
set_button_text = "SET"  # Define set button text
set_button = tk.Button(window, text=set_button_text, font=("Courier", 16, "bold"), bg="white", fg="blue", width=20, height=2, highlightbackground="gray")  # Create set button widget
set_button.grid(padx=5, pady=10, row=2, column=0, columnspan=2)  # Place set button in the window

run_button_text = "RUN"  # Define run button text
run_button = tk.Button(window, text=run_button_text, font=("Courier", 16, "bold"), bg="white", fg="green", width=20, height=2, highlightbackground="gray")  # Create run button widget
run_button.grid(padx=5, pady=10, row=4, column=0, columnspan=2)  # Place run button in the window

stop_button_text = "STOP"  # Define stop button text
stop_button = tk.Button(window, text=stop_button_text, font=("Courier", 16, "bold"), bg="white", fg="red", width=20, height=2, highlightbackground="gray")  # Create stop button widget
stop_button.grid(padx=5, pady=10, row=6, column=0, columnspan=2)  # Place stop button in the window

continue_button_text = "CONTINUE"  # Define continue button text
continue_button = tk.Button(window, text=continue_button_text, font=("Courier", 16, "bold"), bg="white", fg=YELLOW, width=20, height=2, highlightbackground="gray")  # Create continue button widget
continue_button.grid(padx=5, pady=10, row=8, column=0, columnspan=2)  # Place continue button in the window

# Add a text widget for logging
log_text = tk.Text(window, font=("Courier", 16, "bold"), bg="black", fg="yellow", width=22, height=15, highlightbackground="gray")  # Create text widget
log_text.grid(padx=5, pady=10, row=9, column=0, columnspan=2)  # Place text widget in the window

# Adjust column weights to make them fill the space horizontally
window.grid_columnconfigure(2, weight=1)  # Adjust column 2 weight
for col in range(9):  # Adjust weights for columns 2 through 10
    window.grid_columnconfigure(col+2, weight=1)

# Create canvas for displaying images
canvas = tk.Canvas(window, bg="white", borderwidth=0, highlightbackground="gray")  # Create canvas widget
canvas.grid(padx=5, pady=10, row=1, column=2, rowspan=9, columnspan=9, sticky="nsew")  # Place canvas in the window

# Force update to get the correct canvas dimensions
window.update_idletasks()

# Get canvas dimensions
canvas_width = canvas.winfo_width()  # Get canvas width
canvas_height = canvas.winfo_height()  # Get canvas height

# Get canvas center
canvas_cx = canvas_width // 2  # Calculate canvas center x-coordinate
canvas_cy = canvas_height // 2  # Calculate canvas center y-coordinate

# Set rectangle dimensions for visualization purposes
rectangle_width = 500  # Define rectangle width
rectangle_height = 500  # Define rectangle height

# Get the rectangle position
x1 = canvas_cx - rectangle_width // 2  # Calculate rectangle's top-left x-coordinate
y1 = canvas_cy - rectangle_height // 2  # Calculate rectangle's top-left y-coordinate
x2 = canvas_cx + rectangle_width // 2  # Calculate rectangle's bottom-right x-coordinate
y2 = canvas_cy + rectangle_height // 2  # Calculate rectangle's bottom-right y-coordinate

# Place the rectangle on the canvas
canvas.create_rectangle(x1, y1, x2, y2, fill="blue")  # Draw rectangle on canvas

canvas.delete("all")

dummy = data.shepp_logan_phantom()  # Generate a dummy phantom image

# Resize the dummy phantom to fit the canvas properly
dummy = resize(dummy, (350, 350), anti_aliasing=True)  # Resize dummy image

# Convert image to 8-bit for display
dummy_image = img_as_ubyte(dummy)  # Convert image to 8-bit

# Convert numpy array to PIL Image
dummy_image = Image.fromarray(dummy_image)  # Convert numpy array to PIL Image object

# Convert PIL Image to tkinter-compatible image
dummy_image_tk = ImageTk.PhotoImage(dummy_image)  # Convert PIL Image to tkinter-compatible image object

# Get the dimensions of the dummy image
dummy_width = dummy_image_tk.width()  # Get dummy image width
dummy_height = dummy_image_tk.height()  # Get dummy image height

# Get the position to place the dummy image on the canvas
x1_dummy = canvas_cx - dummy_width // 2  # Calculate dummy image's top-left x-coordinate
y1_dummy = canvas_cy - dummy_height // 2  # Calculate dummy image's top-left y-coordinate

# Place the dummy image on the canvas
dummy_image_id = canvas.create_image(x1_dummy, y1_dummy, anchor="nw", image=dummy_image_tk)  # Place dummy image on canvas

# Get the dummy in the camera
diagonal = np.sqrt(dummy_height ** 2 + dummy_width ** 2)  # Calculate diagonal of the dummy image
camera_height = int(np.ceil(diagonal - dummy_height) + 2)  # Calculate camera height
camera_width = int(np.ceil(diagonal - dummy_width) + 2)  # Calculate camera width

# Define global variables to store camera data
camera = None  # Initialize camera array
camera_image = None  # Initialize camera PIL Image
camera_image_tk = None  # Initialize camera tkinter-compatible image

def transition_to_camera_image(step=0):
    """
    Transition function to gradually display the camera image on the canvas.
    
    Args:
        step (int): Current step of the transition animation.
    """
    global camera, camera_image, camera_image_tk
    
    if step <= 100:
        # Calculate the partial width and height of the camera
        partial_height = camera_height * step // 100  # Calculate partial camera height
        partial_width = camera_width * step // 100  # Calculate partial camera width

        new_width = dummy_width + partial_width  # Calculate new width of the camera image
        new_height = dummy_height + partial_height  # Calculate new height of the camera image

        camera = np.zeros((new_height, new_width))  # Create zero-filled camera array
        camera[
            int(np.ceil(partial_height / 2)) : (int(np.ceil(partial_height / 2)) + dummy_height),
            int(np.ceil(partial_width / 2)) : (int(np.ceil(partial_width / 2)) + dummy_width),
        ] = dummy  # Insert dummy image into camera array

        camera_image = img_as_ubyte(camera)  # Convert camera array to 8-bit
        camera_image = Image.fromarray(camera_image)  # Convert camera array to PIL Image
        camera_image_tk = ImageTk.PhotoImage(camera_image)  # Convert PIL Image to tkinter-compatible image

        partial_camera_width = camera_image_tk.width()  # Get partial camera image width
        partial_camera_height = camera_image_tk.height()  # Get partial camera image height

        x1_camera = canvas_cx - partial_camera_width // 2  # Calculate camera image's top-left x-coordinate
        y1_camera = canvas_cy - partial_camera_height // 2  # Calculate camera image's top-left y-coordinate
        
        # Update the dummy image
        canvas.itemconfig(dummy_image_id, image=camera_image_tk)  # Update dummy image on canvas
        canvas.coords(dummy_image_id, x1_camera, y1_camera)  # Update dummy image position on canvas
        
        # Call transition_to_camera_image recursively after a delay
        canvas.after(10, transition_to_camera_image, step + 2)

# Call transition_to_camera_image after a delay of 1000 milliseconds
window.after(1000, transition_to_camera_image)

# Define global variable to store the projections 
projections = []
camera_rotation_tk = None

def rotation_of_the_camera(step=0):

    global camera_rotation_tk

    if step <= 180:
        camera_rotation = rotate(camera, -step, reshape=False)
        camera_rotation /= camera_rotation.max()
        camera_rotation = img_as_ubyte(camera_rotation)
        camera_rotation = Image.fromarray(camera_rotation)

        camera_rotation_tk = ImageTk.PhotoImage(camera_rotation)  # Create a new PhotoImage object

        camera_rotation_width = camera_rotation_tk.width()
        camera_rotation_height = camera_rotation_tk.height()

        x1_camera_rotation = canvas_cx - camera_rotation_width // 2
        y1_camera_rotation = canvas_cy - camera_rotation_height // 2

        canvas.itemconfig(dummy_image_id, image=camera_rotation_tk)  # Update the image on canvas with the new PhotoImage
        canvas.coords(dummy_image_id, x1_camera_rotation, y1_camera_rotation)

        canvas.after(10, rotation_of_the_camera, step + 1)

# Call rotation_of_the_camera after a delay of 1800 milliseconds
window.after(1800, rotation_of_the_camera)

window.mainloop()  # Start the tkinter event loop

