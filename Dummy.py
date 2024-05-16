import numpy as np
from skimage.transform import resize
from skimage import data

class Dummy():
    def __init__(self) -> None:
        self.dummy = data.shepp_logan_phantom()
        self.dummy_width = 350
        self.dummy_height = 350
        self.dummy = resize(self.dummy,(self.dummy_width, self.dummy_height), anti_aliasing=True)
        diagonal = np.sqrt(self.dummy_height ** 2 + self.dummy_width ** 2)
        self.camera_height = int(np.ceil(diagonal - self.dummy_height) + 2)
        self.camera_width = int(np.ceil(diagonal - self.dummy_width) + 2)


