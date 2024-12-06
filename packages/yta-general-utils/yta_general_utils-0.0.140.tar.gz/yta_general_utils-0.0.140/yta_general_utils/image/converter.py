from PIL import Image
from io import BytesIO

import numpy as np
import base64
import cv2


class ImageConverter:
    @classmethod
    def validate_numpy_image(cls, image: np.ndarray):
        """
        This method checks if the provided 'image' is a numpy array, that the
        array has 3 or 4 elements in each cell and if its values are in the
        [0, 255] range or in the [0, 1] (normalized) range. It will raise an
        Exception if any of those conditions are not satisfied.
        """
        if not isinstance(image, np.ndarray):
            raise Exception('The provided "image" parameter is not a numpy np.ndarray instance.')
        
        if image.ndim != 3 or image.shape[2] not in [3, 4]:
            raise Exception('The provided "image" parameter does not represent a RGB or RGBA image.')

        if not np.all((image >= 0) & (image <= 255)):
            raise Exception('The provided numpy array is not a valid image as its values are not between 0 and 255.')

        # TODO: What about '.astype('uint8')', maybe we can check if it is that type (?)

    @classmethod
    def validate_opencv_image(cls, image: np.ndarray):
        """
        This method checks if the provided 'image' is a numpy array, that the
        array has 3 or 4 elements in each cell and if its values are in the
        [0, 255] range or in the [0, 1] (normalized) range. It will raise an
        Exception if any of those conditions are not satisfied.

        An opencv image is just a numpy array with some meta param.
        """
        # The only thing that could change is the message and I don't want
        # to duplicate code for a single 'opencv' word in a message
        return cls.validate_numpy_image(image)

    @classmethod
    def validate_base64_image(cls, image: str):
        """
        This method validates if the provided image is a valid base64 image
        by getting the prefix, the 'base64' str and also trying to decode it.
        It will raise an Exception if the image is not a valid base64 image.
        """
        is_valid = False

        if image.startswith('data:image/') and ';base64,' in image:
            base64_string = image.split(';base64,')[1]
            try:
                base64.b64decode(base64_string, validate = True)
                is_valid = True
            except Exception:
                pass
            
        if not is_valid:
            raise Exception('The provided "image" parameter is not a valid base64 image.')

    @classmethod
    def validate_pillow_image(cls, image: Image.Image):
        if not isinstance(image, Image.Image):
            raise Exception('The provided "image" is not an instance of a Pillow image.')
        
        if image.mode not in ['RGB', 'RGBA']:
            raise Exception('The provided pillow image is not in a valid mode for our software. Valid modes are: "RGB", "RGBA".')
        
    @classmethod
    def numpy_image_to_pil(cls, image: np.ndarray):
        """
        This method checks if the provided 'image' is a numpy array and if its
        values are in the [0, 255] range or in the [0, 1] (normalized) range.
        It will raise an Exception if any of those conditions are not
        satisfied.

        This method will return the image converted into a Pillow image.
        """
        cls.validate_numpy_image(image)
        
        if np.all((image >= 0) & (image <= 1)):
            # TODO: How do I know if the values are normalized or just [0, 255]
            # but with values below 1 (?)
            image = Image.fromarray((image).astype(np.uint8))
        else:
            image = Image.fromarray((image * 255).astype(np.uint8))

        return image
    
    @classmethod
    def numpy_image_to_base64(cls, image: np.ndarray):
        """
        Turns the provided numpy 'image' into a base64 str image.
        """
        cls.validate_numpy_image(image)

        buffer = BytesIO()
        image = cls.numpy_image_to_pil(image).save(buffer, format = 'PNG')
        buffer.seek(0)
        image_bytes = buffer.read()

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_base64_str = f'data:image/png;base64,{image_base64}'

        return image_base64_str
    
    @classmethod
    def numpy_image_to_opencv(cls, image: np.ndarray):
        cls.validate_numpy_image(image)
    
        # This is also a way:
        # pil_data = PIL.Image.open('Image.jpg').convert('RGB')
        # image = numpy.array(pil_data)[:, :, ::-1].copy()

        # I need to know if image is RGB or RGBA
        if image.ndim == 3 and image.shape[2] == 3:   # RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif image.ndim == 2 and image.shape[2] == 4:   # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        
        return image
    
    @classmethod
    def pil_image_to_numpy(cls, image: Image.Image):
        """
        Turns the 'image' to a numpy array. The PIL image must be an
        array produced by the code 'Image.open(image_filename)'.
        """
        cls.validate_pillow_image(image)

        # This will return it as RGB if (4, 4, 3) or as RGBA if (4, 4, 4)
        return np.asarray(image)
    
    @classmethod
    def pil_image_to_base64(cls, image: Image.Image):
        """
        Turns the 'image' to a base64 image by turning it into a numpy
        image first. The PIL image must be an array produced by the code
        'Image.open(image_filename)'.
        """
        cls.validate_pillow_image(image)

        return cls.numpy_image_to_base64(cls.pil_image_to_numpy(image))

    @classmethod
    def pil_image_to_opencv(cls, image: Image.Image):
        """
        Turns the 'image' to a opencv image by turning it into a numpy
        image first. The PIL image must be an array produced by the code
        'Image.open(image_filename)'.
        """
        cls.validate_pillow_image(image)

        return cls.numpy_image_to_opencv(cls.pil_image_to_numpy(image))
    
    @classmethod
    def base64_image_to_pil(cls, image):
        """
        Turns the 'image' to a PIL Image, to be able
        to work with, and returns it.
        """
        cls.validate_base64_image(image)

        return Image.open(BytesIO(base64.b64decode(image)))
    
    @classmethod
    def base64_image_to_numpy(cls, image):
        """
        Turns the 'image' to a numpy image (np.ndarray),
        to be able to work with, and returns it. 
        """
        cls.validate_base64_image(image)
        
        return cls.pil_image_to_numpy(cls.base64_image_to_pil(image))
    
    @classmethod
    def base64_image_to_opencv(cls, image):
        """
        Turns the 'image' to an opencv image by turning it
        into a numpy array first.
        """
        cls.validate_base64_image(image)

        return cls.pil_image_to_base64(cls.base64_image_to_pil)

    @classmethod
    def opencv_image_to_numpy(cls, image: np.ndarray):
        """
        Turns the 'image' to an opencv image by turning it
        into a numpy array first.
        """
        cls.validate_opencv_image(image)

        # An opencv image is just a numpy array with a meta param

        # I need to know if image is RGB or RGBA
        if image.ndim == 3 and image.shape[2] == 3:   # RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif image.ndim == 2 and image.shape[2] == 4:   # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        
        return image

    @classmethod
    def opencv_image_to_pillow(cls, image: np.ndarray):
        """
        Turns the 'image' to a pillow image by turning it
        into a numpy array first.
        """
        cls.validate_opencv_image(image)

        return cls.numpy_image_to_pil(cls.opencv_image_to_numpy(image))
    
    @classmethod
    def opencv_image_to_base64(cls, image: np.ndarray):
        """
        Turns the 'image' to a base64 image by turning it
        into a numpy array first.
        """
        cls.validate_opencv_image(image)

        return cls.numpy_image_to_base64(cls.opencv_image_to_numpy(image))

