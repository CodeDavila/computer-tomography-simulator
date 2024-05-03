import tkinter as tk

# Assuming WINDOW_WIDTH and WINDOW_HEIGHT are defined in constants.py
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW

window = tk.Tk()
window.title("CT machine")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.resizable(False, False)
window.configure(bg="gray")
window.attributes("-alpha", 0.95)

label_text = "Computed Tomography Scanner"
label = tk.Label(window, text=label_text, font=("Courier", 16), bg="gray", fg="black")
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

# Create rectangle within the canvas
canvas.create_rectangle(10, 10, 490, 490, fill="blue")

window.mainloop()

