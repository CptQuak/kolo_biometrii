import numpy as np
from PIL import Image
import io

class ImageLoader:
    def __init__(self):
        pass

    def img_to_bytes(self, img):
        '''
        img to bytes for viewing
        '''
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def load_image(self, file_path, target, im_size):
        '''
        Given img path, img window, reads, resizes, transforms to bytes and displays window
        '''
        img = Image.open(file_path).resize((im_size, im_size))
        data = self.img_to_bytes(img)
        target.update(data = data)
        return img