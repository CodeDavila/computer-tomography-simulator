import numpy as np
from skimage.transform import resize
from skimage import data
# dummy
class Dummy():
    def __init__(self) -> None:
        # Initialize the Dummy class
        # Generate a Shepp-Logan phantom as the dummy image
        self.dummy = data.shepp_logan_phantom()
        # Define dimensions for resizing
        self.dummy_width = 350
        self.dummy_height = 350
        # Resize the dummy image
        self.dummy = resize(self.dummy, (self.dummy_width, self.dummy_height), anti_aliasing=True)
        # Calculate diagonal length
        diagonal = np.sqrt(self.dummy_height ** 2 + self.dummy_width ** 2)
        # Calculate camera dimensions based on dummy image dimensions and diagonal length
        self.camera_height = int(np.ceil(diagonal - self.dummy_height) + 2)
        self.camera_width = int(np.ceil(diagonal - self.dummy_width) + 2)
        
