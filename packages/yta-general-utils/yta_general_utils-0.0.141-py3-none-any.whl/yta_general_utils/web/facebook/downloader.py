
from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.downloader import get_file
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Union


def get_facebook_video(url: str, output_filename: Union[str, None] = None):
    """
    Gets the Facebook video (reel) from the provided 'url' (if valid)
    and returns its data or stores it locally as 'output_filename' if
    provided.
    """
    DOWNLOAD_FACEBOOK_VIDEO_URL = 'https://fdownloader.net/en/facebook-reels-downloader'

    scrapper = ChromeScrapper()
    scrapper.go_to_web_and_wait_util_loaded(DOWNLOAD_FACEBOOK_VIDEO_URL)

    # We need to wait until video is shown
    url_input = scrapper.find_element_by_id('s_input')
    url_input.send_keys(url)
    url_input.send_keys(Keys.ENTER)

    # We need to click in the upper left image to activate vid popup
    image_container = scrapper.find_element_by_class_waiting('div', 'image-fb open-popup')
    image = image_container.find_element(By.TAG_NAME, 'img')
    image.click()

    #video_element = scrapper.find_element_by_element_type_waiting('video')
    video_element = scrapper.find_element_by_id_waiting('vid')
    video_source_url = video_element.get_attribute('src')

    return get_file(video_source_url, output_filename)