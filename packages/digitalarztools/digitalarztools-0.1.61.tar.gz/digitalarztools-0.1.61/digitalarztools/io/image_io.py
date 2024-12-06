import os
from io import BytesIO

import numpy as np
from PIL import Image

from digitalarztools.io.file_io import FileIO


class ImageIO:
    @classmethod
    def create_empty_image(cls, size_x, size_y):
        blank_image = np.zeros([size_x, size_y, 4], dtype=np.uint8)
        return cls.create_image(blank_image)

    @staticmethod
    def create_image(np_array, format="PNG", f_name=None):
        img = Image.fromarray(np_array)
        if f_name:
            fp = os.path.join('media/temp', f_name)
            FileIO.mkdirs(fp)
            img.save(fp, format)

        buffer = BytesIO()
        img.save(buffer, format=format)  # Enregistre l'image dans le buffer
        # return "data:image/PNG;base64," + base64.b64encode(buffer.getvalue()).decode()
        return buffer  # .getvalue()
