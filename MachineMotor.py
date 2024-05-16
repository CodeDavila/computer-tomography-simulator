import tkinter as tk
import numpy as np
from scipy.ndimage import rotate
from ImageProcessor import ImageProcessor

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


