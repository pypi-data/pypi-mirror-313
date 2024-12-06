from yta_general_utils.temp import create_temp_filename
from yta_general_utils.checker.url import verify_image_url
from yta_general_utils.file.filename import replace_file_extension
from yta_general_utils.downloader.utils import download_file
from typing import Union

import requests


def download_image(url: str, output_filename: Union[str, None] = None):
    """
    Downloads the image from the provided 'url' if valid (it raises an
    Exception if not). If user provides 'output_filename' it could be
    fixed according to the real image extension. If it is not provided,
    a new temporary filename will be created. In both cases, the final
    'output_filename' is returned.
    """
    image_extension = verify_image_url(url)
    if not image_extension:
        raise Exception('Url "' + url + '" is not a valid image url.')
    
    if not output_filename:
        output_filename = create_temp_filename(f'image{image_extension}')
    else:
        # Force the received image extension in headers content-type
        if not output_filename.endswith(image_extension):
            output_filename = replace_file_extension(output_filename, image_extension)
    
    # TODO: Maybe we want to return the content instead of the filename
    # so, if they don't provide 'output_filename' we could return the
    # content instead, and only download it if 'output_filename' is 
    # provided (fixing it if is wrong) and return the final 
    # 'output_filename' in this last case.
    download_file(url, output_filename)

    return output_filename

def download_image_2(url: str, output_filename: str):
    """
    Downloads an image from the provided 'url' if possible.

    # TODO: I need to check this one and compare with the
    # other method so maybe preserve only one (?)
    """
    if not url:
        return None

    if not output_filename:
        return None
    
    import shutil
    
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(output_filename,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', output_filename)
    else:
        print('Image Couldn\'t be retrieved')