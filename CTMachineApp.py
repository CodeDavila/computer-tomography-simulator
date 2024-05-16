import tkinter as tk
from PIL import Image, ImageTk
from Dummy import Dummy
from ImageProcessor import ImageProcessor
from MachineMotor import MachineMotor

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW

class CTMachineApp:
    def __init__(self, master) -> None:
        self.master = master
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.create_widgets()
        self.set_flag = False
        self.run_flag = False

    def create_widgets(self):
        self.master.title("CT machine")
        self.master.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.master.resizable(False, False)
        self.master.configure(bg="gray")
        self.master.attributes("-alpha", 0.95)
        self.create_labels()
        self.create_buttons()
        self.create_log_text()
        self.create_canvas()
        self.draw_entry()

    def create_labels(self):
        label_text = "Computed Tomography Scanner"
        label = tk.Label(self.master, text=label_text, font=("Courier", 24), bg="gray", fg="white")
        label.grid(padx=10, pady=10, row=0, column=0, columnspan=11)

    def create_buttons(self):
        buttons_data = [
            ("SET", "blue", self.on_set_button_click),
            ("RUN", "green", self.on_run_button_click),
            ("STOP", "red", self.on_stop_button_click),
            ("CONTINUE", YELLOW, self.on_continue_button_click)
        ]
        for i, (text, color, command) in enumerate(buttons_data):
            button = tk.Button(self.master, text=text, font=("Courier", 16, "bold"),
                               bg="white", fg=color, width=20, height=2,
                               highlightbackground="gray", command=command)
            button.grid(padx=5, pady=10, row=2+i*2, column=0, columnspan=2)

    def create_log_text(self):
        self.log_text = tk.Text(self.master, font=("Courier", 16, "bold"), bg="black", fg="yellow",
                                width=22, height=15, highlightbackground="gray")
        self.log_text.grid(padx=5, pady=10, row=9, column=0, columnspan=2)

    def create_canvas(self):
        self.master.grid_columnconfigure(2, weight=1)
        for col in range(9):
            self.master.grid_columnconfigure(col+2, weight=1)
        self.canvas = tk.Canvas(self.master, bg="white", borderwidth=0, highlightbackground="gray")
        self.canvas.grid(padx=5, pady=10, row=1, column=2, rowspan=9, columnspan=9, sticky="nsew")
        self.master.update_idletasks()

    def canvas_center(self):
        canvas_cx = self.canvas.winfo_width() // 2
        canvas_cy = self.canvas.winfo_height() // 2
        return canvas_cx, canvas_cy
    
    def draw_entry(self) -> None:
        try:
            image = Image.open("ct_entry.png")
            image = image.resize((500, 500))
            self.image_entry = ImageTk.PhotoImage(image)
            image_width = self.image_entry.width()
            image_height = self.image_entry.height()
            cx, cy = self.canvas_center()
            x = cx - image_width // 2
            y = cy - image_height // 2
            self.image_entry_ID = self.canvas.create_image(x, y, anchor="nw", image=self.image_entry)
        except Exception as e:
            print("Error :", e)

    def draw_dummy_image(self):
        cx, cy = self.canvas_center()
        self.dummy = Dummy()
        dummy_tk, x, y = ImageProcessor.process_image_tk(self.dummy.dummy, cx, cy)
        self.imageID = self.canvas.create_image(x, y, anchor="nw", image=dummy_tk)

    def update_canvas(self, image_tk, x, y, fun, steps):
        self.canvas.itemconfig(self.imageID, image=image_tk)
        self.canvas.coords(self.imageID, x, y)
        self.canvas.after(10, fun, steps)

    def on_set_button_click(self):
        if not self.set_flag:
            self.set_flag = True
            self.canvas.delete(self.image_entry_ID)
            self.draw_dummy_image()
            self.machine = MachineMotor(self)
            self.master.after(500, self.machine.transition_to_camera_image)

    def on_run_button_click(self):
        if self.set_flag and not self.run_flag:
            self.run_flag = True
            self.machine.rotation_of_the_camera()
            self.master.wait_variable(self.machine.sync)
            self.machine.reconstruction_of_the_image()
            self.master.wait_variable(self.machine.sync)
            self.machine.crop_reconstruction()

    # TODO:
    # - Implement functionality for the 'on_stop_button_click' method.
    # - Implement functionality for the 'on_continue_button_click' method.
    def on_stop_button_click(self):
        pass

    def on_continue_button_click(self):
        pass

    def run_app(self):
        self.master.mainloop()


