from PIL import Image


# TODO: Create a class two wrap this
# TODO: Improve this method to receive not only a image_filename (str)
# but also Image, numpy, etc.
def is_valid_image(image_filename):
    """
    Tries to open the 'image_filename' provided to check if it is corrupt or it is valid. It 
    returns True if the provided image is valid, or False if is corrupt.
    """
    try:
        im = Image.open(image_filename)
        im.verify()
        im.close()
    except (IOError, OSError, Image.DecompressionBombError) as e:
        return False
        
    return True

def has_transparency(image: Image):
    """
    Checks if the provided image (read with pillow) has transparency.
    """
    # TODO: What about 'image' filename instead of Image PIL (?)
    if image.info.get("transparency", None) is not None:
        return True
    if image.mode == "P":
        transparent = image.info.get("transparency", -1)
        for _, index in image.getcolors():
            if index == transparent:
                return True
    elif image.mode == "RGBA":
        extrema = image.getextrema()
        if extrema[3][0] < 255:
            return True

    return False