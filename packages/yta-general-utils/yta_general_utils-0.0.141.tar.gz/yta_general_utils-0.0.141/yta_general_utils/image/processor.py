from yta_general_utils.image.color.picker import ColorPicker
from PIL import Image
from subprocess import run

import numpy as np
import skimage.exposure
import cv2


# TODO: This is related to Image so multimedia (?)
def get_green_screen_position(image_filename):
    """
    Detects the green screen color of the provided 'image_filename' and then looks for
    the upper left corner and the bottom right corner.

    This method return an object containing 'ulx', 'uly', 'drx', 'dry' coords. It also
    returns the 'rgb_color' most common green color as an (r, g, b).

    This will return None in ['rgb_color'] field if no green color detected.
    """
    green_rgb_color = ColorPicker.get_most_common_rgb_color(image_filename)

    image = Image.open(image_filename).convert('RGB')

    upper_left = {
        'x': 99999,
        'y': 99999,
    }
    down_right = {
        'x': -1,
        'y': -1,
    }

    for x in range(image.width):
        for y in range(image.height):
            rgb_color = (r, g, b) = image.getpixel((x, y))

            if rgb_color == green_rgb_color:
                if x < upper_left['x']:
                    upper_left['x'] = x
                if y < upper_left['y']:
                    upper_left['y'] = y
                
                """
                if x <= upper_left['x'] and y <= upper_left['y']:
                    upper_left = {
                        'x': x,
                        'y': y,
                    }
                """

                if x > down_right['x']:
                    down_right['x'] = x
                if y > down_right['y']:
                    down_right['y'] = y

                """
                if x >= down_right['x'] and y >= down_right['y']:
                    down_right = {
                        'x': x,
                        'y': y,
                    }
                """

    # We apply some margin to make sure we fit the green screen
    MARGIN = 2

    if (upper_left['x'] - MARGIN) > 0:
        upper_left['x'] -= MARGIN
    else:
        upper_left['x'] = 0

    if (upper_left['y'] - MARGIN) > 0:
        upper_left['y'] -= MARGIN
    else:
        upper_left['y'] = 0

    if (down_right['x'] + MARGIN) < 1920:
        down_right['x'] += MARGIN
    else:
        down_right['x'] = 1920

    if (down_right['y'] + MARGIN) < 1080:
        down_right['y'] += MARGIN
    else:
        down_right['y'] = 1080

    return {
        'rgb_color': green_rgb_color,
        'ulx': upper_left['x'],
        'uly': upper_left['y'],
        'drx': down_right['x'],
        'dry': down_right['y'],
    }

def remove_background(image_filename, output_filename):
    """
    Removes the background of the provided 'image_filename' by using the 
    'backgroundremover' open library that is included in a comment.
    """
    # It uses (https://github.com/nadermx/backgroundremover?referral=top-free-background-removal-tools-apis-and-open-source-models)
    # That uses U2Net (https://medium.com/axinc-ai/u2net-a-machine-learning-model-that-performs-object-cropping-in-a-single-shot-48adfc158483)
    command_parameters = ['backgroundremover', '-i', image_filename, '-o', output_filename]

    run(command_parameters)

    # TODO: This below seems to work (as shown in this 
    # commit https://github.com/nadermx/backgroundremover/commit/c590858de4c7e75805af9b8ecdd22baf03a1368f)
    """
    from backgroundremover.bg import remove
    def remove_bg(src_img_path, out_img_path):
        model_choices = ["u2net", "u2net_human_seg", "u2netp"]
        f = open(src_img_path, "rb")
        data = f.read()
        img = remove(data, model_name=model_choices[0],
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_structure_size=10,
                    alpha_matting_base_size=1000)
        f.close()
        f = open(out_img_path, "wb")
        f.write(img)
        f.close()
    """

def remove_background_video(video_filename, output_filename):
    # TODO: Move to 'video_utils'
    # TODO: This is too demanding as I cannot process it properly
    # Output must end in .mov to preserve transparency
    command_parameters = ['backgroundremover', '-i', video_filename, '-tv', '-o', output_filename]

    run(command_parameters)

def remove_green_screen(image_filename, output_filename):
    # From https://stackoverflow.com/a/72280828
    # load image
    img = cv2.imread(image_filename)

    # convert to LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # extract A channel
    A = lab[:,:,1]

    # threshold A channel
    thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # blur threshold image
    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX = 5, sigmaY = 5, borderType = cv2.BORDER_DEFAULT)

    # stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range = (127.5, 255), out_range = (0, 255)).astype(np.uint8)

    # add mask to image as alpha channel
    result = img.copy()
    result = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)
    result[:,:,3] = mask

    # save output
    cv2.imwrite(output_filename, result)
