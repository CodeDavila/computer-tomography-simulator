from PIL import Image, ImageTk
from skimage.util import img_as_ubyte

class ImageProcessor:
    @staticmethod
    def process_image_tk(image, canvas_cx, canvas_cy):
        """
        Process the given image for displaying on a Tkinter canvas.

        Parameters:
            image (numpy.ndarray): The input image as a NumPy array.
            canvas_cx (int): The x-coordinate of the center of the canvas.
            canvas_cy (int): The y-coordinate of the center of the canvas.

        Returns:
            tuple: A tuple containing the processed Tkinter PhotoImage, and the coordinates (x, y)
            where the image should be placed on the canvas.
        """
        # Normalize image
        den = image.max() - image.min()
        num = image - image.min()
        image = num / den
        # Convert image to uint8 format
        image = img_as_ubyte(image)
        # Convert image to PIL Image
        image = Image.fromarray(image)
        # Convert PIL Image to Tkinter PhotoImage
        image_tk = ImageTk.PhotoImage(image)
        # Get dimensions of the Tkinter PhotoImage
        image_width = image_tk.width()
        image_height = image_tk.height()
        # Calculate coordinates for placing the image on the canvas
        x = canvas_cx - image_width // 2
        y = canvas_cy - image_height // 2
        return image_tk, x, y
