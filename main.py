import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from scipy.ndimage import rotate
from skimage.transform import resize
from skimage import data
from skimage.util import img_as_ubyte

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
YELLOW = "#EE9626"

class ImageProcessor:
    @staticmethod
    def process_image_tk(image, canvas_cx, canvas_cy):
        den = image.max() - image.min()
        num = image - image.min()
        image = num/den
        image = img_as_ubyte(image)
        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image)
        image_width = image_tk.width()
        image_height = image_tk.height()
        x = canvas_cx - image_width // 2
        y = canvas_cy - image_height // 2
        return image_tk, x, y

class Dummy():
    def __init__(self) -> None:
        self.dummy = data.shepp_logan_phantom()
        self.dummy_width = 350
        self.dummy_height = 350
        self.dummy = resize(self.dummy,(self.dummy_width, self.dummy_height), anti_aliasing=True)
        diagonal = np.sqrt(self.dummy_height ** 2 + self.dummy_width ** 2)
        self.camera_height = int(np.ceil(diagonal - self.dummy_height) + 2)
        self.camera_width = int(np.ceil(diagonal - self.dummy_width) + 2)


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

    def on_stop_button_click(self):
        pass

    def on_continue_button_click(self):
        pass

    def run_app(self):
        self.master.mainloop()

class MachineMotor:
    def __init__(self, master) -> None:
        self.master = master
        self.camera = None
        self.camera_tk = None
        self.camera_rotation_tk = None
        self.projections_list = []
        self.reconstruction = np.array((0,0))
        self.reconstruction_tk = None
        self.cut = None
        self.cut_tk = None
        self.sync = tk.BooleanVar(value=False)

    def transition_to_camera_image(self, step = 0):        
        if step <= 100:
            pH = self.master.dummy.camera_height * step // 100
            pW = self.master.dummy.camera_width * step // 100
            new_height = self.master.dummy.dummy_height + pH
            new_width = self.master.dummy.dummy_width + pW
            self.camera = np.zeros((new_height, new_width))
            self.camera[
                    int(np.ceil(pH/2)) : (int(np.ceil(pH/2)) + self.master.dummy.dummy_height),
                    int(np.ceil(pW/2)) : (int(np.ceil(pW/2)) + self.master.dummy.dummy_width),
            ] = self.master.dummy.dummy
            cx, cy = self.master.canvas_center()
            self.camera_tk, x, y = ImageProcessor.process_image_tk(self.camera, cx, cy)
            self.master.update_canvas(self.camera_tk, x, y, self.transition_to_camera_image, steps = step+2)

    def rotation_of_the_camera(self, step = 1):
        if step <= 360:
            if step <= 180:
                camera_rotation = rotate(self.camera, -step, reshape=False)
                column_sums = np.sum(camera_rotation, axis=0)
                self.projections_list.append(column_sums)
            elif step < 360:
                camera_rotation = rotate(self.camera, -180+step%180, reshape=False)
            else:
                camera_rotation = self.camera
                self.sync.set(not self.sync)
            cx, cy = self.master.canvas_center()
            self.camera_rotation_tk, x, y = ImageProcessor.process_image_tk(camera_rotation, cx, cy)
            self.master.update_canvas(self.camera_rotation_tk, x, y, self.rotation_of_the_camera, steps = step+1)

    def reconstruction_of_the_image(self):
        self.projections = np.array(self.projections_list)
        self.n = self.projections.shape[1]
        self.th = np.pi/2 - np.deg2rad(np.linspace(1, 180, self.projections.shape[0]))
        self.center = (self.n-1)/2
        x = np.arange(0, self.n)
        y = np.arange(0, self.n)
        X, Y = np.meshgrid(x, y)
        self.xpr = X - self.center
        self.ypr = Y - self.center
        self.reconstruction = np.zeros((self.n, self.n))
        w = np.linspace(-np.pi, np.pi-(2*np.pi)/self.n, self.n)
        self.my_filter = np.abs(np.sin(w))
        self.reconstruction_process()
        
    def reconstruction_process(self, step = 0):
        if step < self.projections.shape[0]:
            reconstruction_aux = np.ones((self.n, self.n))
            indx  = np.round(self.center + self.xpr * np.sin(self.th[step]) - self.ypr * np.cos(self.th[step])).astype(int)
            valIndx = np.where((indx >= 0) & (indx < self.n))
            indx = indx[valIndx]
            projectionsFFT = np.fft.fft(self.projections[step, :])
            filteredProjectionsDF = projectionsFFT * self.my_filter
            filteredProjectionsDT = np.fft.ifft(filteredProjectionsDF)
            reconstruction_aux[valIndx] = np.real(filteredProjectionsDT[indx])
            self.reconstruction += reconstruction_aux
            cx, cy = self.master.canvas_center()
            self.reconstruction_tk, x, y = ImageProcessor.process_image_tk(self.reconstruction, cx, cy)
            self.master.update_canvas(self.reconstruction_tk, x, y, self.reconstruction_process, steps = step+1)
        else:
            self.sync.set(not self.sync)

    def crop_reconstruction(self, step = 100):
        if step >= 0:
            pH = self.master.dummy.camera_height * step // 100
            pW = self.master.dummy.camera_width * step // 100
            new_height = self.master.dummy.dummy_height + pH
            new_width = self.master.dummy.dummy_width + pW
            self.cut = np.zeros((new_height, new_width))
            self.cut = self.reconstruction[
                int(np.ceil(self.center - new_height/2)) : (int(np.ceil(self.center + new_height/2))),
                int(np.ceil(self.center - new_width/2)) : (int(np.ceil(self.center + new_width/2))),
            ]
            cx, cy = self.master.canvas_center()
            self.cut_tk, x, y = ImageProcessor.process_image_tk(self.cut, cx, cy)
            self.master.update_canvas(self.cut_tk, x, y, self.crop_reconstruction, steps = step-2)

def main():
    root = tk.Tk()
    app = CTMachineApp(root)
    app.run_app()

if __name__ == "__main__":
    main()

