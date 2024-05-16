from PIL import Image, ImageTk
from skimage.util import img_as_ubyte

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

