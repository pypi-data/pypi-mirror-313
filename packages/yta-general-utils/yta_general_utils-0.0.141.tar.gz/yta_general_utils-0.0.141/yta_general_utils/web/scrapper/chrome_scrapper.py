from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Union

import time


class ChromeScrapper:
    gui = True
    ad_blocker = True
    disable_popups_and_cookies = True
    additional_options = []
    max_page_load_waiting_time = 10
    options = None
    # TODO: Maybe make 'driver' private attribute in ChromeScrapper to
    # avoid exposing it
    driver = None

    def __init__(self, gui: bool = False, ad_blocker: bool = True, disable_popups_and_cookies: bool = True, additional_options = [], max_page_load_waiting_time: float = 10):
        # TODO: Make more customizable accepting ad_blocker extension name
        # and stuff like that
        self.gui = gui
        self.ad_blocker = ad_blocker
        self.disable_popups_and_cookies = disable_popups_and_cookies
        self.additional_options = additional_options
        self.max_page_load_waiting_time = max_page_load_waiting_time

        self.__init_options()
        self.__init_driver()

    def __del__(self):
        try:
            self.driver.close()
        finally:
            self.driver = None

    def __init_options(self):
        """
        Initializes the Google Chrome options and returns them.
        """
        if not self.options:
            # TODO: This must be dynamic and/or given by user
            CHROME_EXTENSIONS_ABSOLUTEPATH = 'C:/Users/dania/AppData/Local/Google/Chrome/User Data/Profile 2/Extensions/'
            # TODO: Extensions versions are updated, so check below line
            AD_BLOCK_ABSOLUTEPATH = CHROME_EXTENSIONS_ABSOLUTEPATH + 'cjpalhdlnbpafiamejdnhcphjbkeiagm/1.59.0_0'
            # TODO: What if 'import undetected_chromedriver.v2 as uc'? Try it

            options = Options()
            
            # TODO: Make this a dynamic option that can be passed through __init__
            option_arguments = ['window-size=1920,1080']
            # option_arguments = ['--start-maximized']

            if len(self.additional_options) > 0:
                for additional_option in self.additional_options:
                    option_arguments.append(additional_option)

            if not self.gui:
                option_arguments.append('--headless=new')

            if self.ad_blocker:
                # This loads the ad block 'uBlock' extension that is installed in my pc
                option_arguments.append('load-extension=' + AD_BLOCK_ABSOLUTEPATH)
            
            # Load user profile
            option_arguments.append('user-data-dir=C:/Users/dania/AppData/Local/Google/Chrome/User Data/Profile 2')

            # Ignore certs
            option_arguments.append('--ignore-certificate-errors')
            option_arguments.append('--ignore-ssl-errors')
            option_arguments.append('--ignore-certificate-errors-spki-list')

            for argument in option_arguments:
                options.add_argument(argument)

            if self.disable_popups_and_cookies:
                # TODO: Separate this into specific options, not all together. One is for cookies,
                # another one is for popups... Separate them, please
                # This disables popups, cookies and that stuff
                options.add_experimental_option('prefs', {
                    'excludeSwitches': ['enable-automation', 'load-extension', 'disable-popup-blocking'],
                    'profile.default_content_setting_values.automatic_downloads': 1,
                    'profile.default_content_setting_values.media_stream_mic': 1
                })

            self.options = options

        return self.options
    
    def __init_driver(self):
        """
        Initializes the Google Chrome driver and returns it.
        """
        if not self.driver:
            self.driver = webdriver.Chrome(options = self.options)
            # We force to start a new session due to some problems
            #self.driver.start_session({})

        return self.driver
    
    def go_to_web_and_wait_util_loaded(self, url: str):
        """
        Navigates to the provided 'url' and checks continuously
        if the page has been loaded or not. It will wait for
        'max_page_load_waiting_time' seconds set when the
        ChromeScrapper object was created.

        This method will return True in the moment the page is 
        loaded.
        """
        if not url:
            raise Exception('No "url" provided.')
    
        CHECK_TIME = 0.25

        try:
            self.driver.get(url)

            page_state = 'loading'
            cont = 0
            while page_state != 'complete' and cont < (self.max_page_load_waiting_time / CHECK_TIME):
                time.sleep(CHECK_TIME)
                page_state = self.driver.execute_script('return document.readyState;')
                cont += 1

            if page_state == 'loading':
                return False
            
            return True

        except:
            self.driver.close()
            self.driver = None

    def wait(self, seconds: float):
        """
        Waits for the provided 'time' seconds. Value must be between
        0 and 60.
        """
        if not seconds:
            raise Exception('No "seconds" provided.')
        
        if seconds < 0:
            raise Exception('Provided "seconds" must be greater than 0.')
        
        if seconds > 60:
            seconds = 60

        time.sleep(seconds)

    def press_ctrl_letter(self, letter: str = 'c'):
        """
        Holds the Ctrl key down, presses the provided 'letter' and 
        releases the Ctrl key. This is useful for Ctrl+C, Ctrl+V
        combinations.
        """
        # TODO: Check if letter is valid
        if not letter:
            raise Exception('No "letter" provided.')
        
        letter = letter[0]

        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(letter).key_up(Keys.CONTROL).perform()

    def press_ctrl_letter_on_element(self, letter: str, element: WebElement):
        """
        Presses the Ctrl + provided 'letter' in the also provided
        'element'. Useful to paste text into text elements.
        """
        if not letter:
            raise Exception('No "letter" provided.')
        
        if not element:
            raise Exception('No "element" provided.')
        
        letter = letter[0]

        element.send_keys(Keys.CONTROL, letter)

    def press_ctrl_c(self):
        self.press_ctrl_letter('c')

    def press_ctrl_c_on_element(self, element: WebElement):
        self.press_ctrl_letter_on_element('c', element)

    def press_ctrl_x(self):
        self.press_ctrl_letter('x')

    def press_ctrl_x_on_element(self, element: WebElement):
        self.press_ctrl_letter_on_element('x', element)

    def press_ctrl_v(self):
        self.press_ctrl_letter('v')

    def press_ctrl_v_on_element(self, element: WebElement):
        self.press_ctrl_letter_on_element('v', element)

    def press_ctrl_a(self):
        self.press_ctrl_letter('a')

    def press_ctrl_a_on_element(self, element: WebElement):
        self.press_ctrl_letter_on_element('a', element)

    def press_key_x_times(self, key: Keys, times: int):
        """
        Presses the provided 'key' 'times' times one behind
        the other one. This method is useful to use TAB,
        ENTER or keys like that a lot of times.
        """
        # TODO: Check times is valid
        actions_chain = ActionChains(self.driver)
        for i in range(times):
            actions_chain.send_keys(key)
        actions_chain.perform()

    def find_element_by_id(self, id: str, element: Union[WebElement, None] = None):
        """
        This method returns the first WebElement found with
        the provided 'id' or None if not found.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.
        """
        elements = self.find_elements_by_id(id, element)

        if not elements:
            return None
        
        return elements[0]
    
    def find_element_by_id_waiting(self, id: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' with also provided 'id' is visible and 
        returns it if it becomes visible in the 'time' seconds 
        of waiting. It returns None if not.
        """
        if not id:
            raise Exception('No "id" provided.')
        
        return self.__find_element_by_waiting(By.ID, id, time)

    def find_elements_by_id(self, id: str, element: Union[WebElement, None] = None):
        """
        This method returns an array containing the WebElements
        found with the provided 'id'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.
        """
        if not id:
            raise Exception('No "id" provided.')
        
        if element:
            return element.find_elements(By.ID, id)
        
        return self.driver.find_elements(By.ID, id)

    def find_element_by_text(self, element_type: str, text: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(text(), 'text')]' 
        structure to find the element, useful for buttons that 
        have 'Save' text or things similar.

        You can use 'element_type' = 'button' and 'text' =
        'Guardar' to find the elements like this one:
        <button>Guardar</button>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'text'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        elements = self.find_elements_by_text(element_type, text, element)
        
        if len(elements) > 0:
            return elements[0]
        
        return None

    def find_element_by_text_waiting(self, element_type: str, text: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and 'text' is visible and returns it if 
        it becomes visible in the 'time' seconds of waiting. It 
        returns None if not.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not text:
            raise Exception('No "text" provided.')

        return self.__find_element_by_waiting(By.XPATH, "//" + element_type + "[contains(text(), '" + text + "')]", time)
    
    def find_elements_by_text(self, element_type: str, text: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(text(), 'text')]' 
        structure to find the element, useful for buttons that 
        have 'Save' text or things similar.

        You can use 'element_type' = 'button' and 'text' =
        'Guardar' to find the elements like this one:
        <button>Guardar</button>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'text'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not text:
            raise Exception('No "text" provided.')
        
        if element:
            return element.find_elements(By.XPATH, "//" + element_type + "[contains(text(), '" + text + "')]")

        return self.driver.find_elements(By.XPATH, "//" + element_type + "[contains(text(), '" + text + "')]")
    
    def find_element_by_class(self, element_type: str, class_str: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(@class, 'class_str')]' 
        structure to find the element, useful for divs with a
        specific class or similar.

        You can use 'element_type' = 'div' and 'class_str' =
        'container-xl' to find the elements like this one:
        <div class='container-xl'>content</div>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'class_str'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        elements = self.find_elements_by_class(element_type, class_str, element)
        
        if len(elements) > 0:
            return elements[0]
        
        return None
    
    def find_element_by_class_waiting(self, element_type: str, class_str: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and class is visible and returns it if it
        becomes visible in the 'time' seconds of waiting. It 
        returns None if not.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not class_str:
            raise Exception('No "class_str" provided.')
        
        return self.__find_element_by_waiting(By.XPATH, "//" + element_type + "[contains(@class, '" + class_str + "')]", time)

    def find_elements_by_class(self, element_type: str, class_str: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[contains(@class, 'class_str')]' 
        structure to find the element, useful for divs with a
        specific class or similar.

        You can use 'element_type' = 'div' and 'class_str' =
        'container-xl' to find the elements like this one:
        <div class='container-xl'>content</div>

        You can also use the wildcard '*'  to find any type of
        element with the specific provided 'class_str'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not class_str:
            raise Exception('No "class_str" provided.')

        if element:
            return element.find_elements(By.XPATH, "//" + element_type + "[contains(@class, '" + class_str + "')]")
        
        return self.driver.find_elements(By.XPATH, "//" + element_type + "[contains(@class, '" + class_str + "')]")

    def find_element_by_custom_tag(self, element_type: str, custom_tag: str, custom_tag_value: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[@custom-tag='custom_value')]' 
        structure to find the element, useful for divs with a
        specific tag or similar.

        You can use the wildcard '*'  to find any type of
        element with the specific provided 'custom_tag'.

        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns the first found WebElement if 
        existing or None if not found.
        """
        elements = self.find_elements_by_custom_tag(element_type, custom_tag, custom_tag_value, element)
        
        if len(elements) > 0:
            return elements[0]
        
        return None

    def find_element_by_custom_tag_waiting(self, element_type: str, custom_tag: str, custom_tag_value: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' and custom tag is visible and returns it 
        if it becomes visible in the 'time' seconds of waiting.
        It returns None if not.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not custom_tag:
            raise Exception('No "class_str" provided.')
        
        tag = '@' + custom_tag
        if custom_tag_value:
            tag += "='" + custom_tag_value + "'"

        return self.__find_element_by_waiting(By.XPATH, "//" + element_type + "[" + tag + "]", time)

    def find_elements_by_custom_tag(self, element_type: str, custom_tag: str, custom_tag_value: str, element: Union[WebElement, None] = None):
        """
        This method uses the 'By.XPATH' finding elements method
        with the '//element_type[@custom-tag='custom_value')]' 
        structure to find the element, useful for divs with a
        specific tag or similar.

        You can use the wildcard '*'  to find any type of
        element with the specific provided 'custom_tag'.
        
        If you provide the 'element' parameter, the search will 
        be in that element instead of the whole web page.

        This method returns an array with all the found elements
        or empty if not found.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        if not custom_tag:
            raise Exception('No "class_str" provided.')
        
        # @custom-tag or @custom-tag='something'
        tag = '@' + custom_tag
        if custom_tag_value:
            tag += "='" + custom_tag_value + "'"

        if element:
            return element.find_elements(By.XPATH, "//" + element_type + "[" + tag + "]")

        return self.driver.find_elements(By.XPATH, "//" + element_type + "[" + tag + "]")

    def find_element_by_element_type(self, element_type: str, element: Union[WebElement, None] = None):
        """
        Returns the elements found with the provided 'element_type' tag, that
        is the tag name ('span', 'div', etc.). If you provide the 'element' 
        parameter, the search will be in that element instead of the whole
        web page.
        """
        # TODO: Document
        elements = self.find_elements_by_element_type(element_type, element)
        
        if len(elements) > 0:
            return elements[0]
        
        return None
    
    def find_element_by_element_type_waiting(self, element_type: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 
        'element_type' tag is visible and returns it if it becomes
        visible in the 'time' seconds of waiting. It returns None
        if not.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        return self.__find_element_by_waiting(By.TAG_NAME, element_type, time)
        
    def find_elements_by_element_type(self, element_type: str, element: Union[WebElement, None] = None, only_first_level: bool = False):
        """
        Returns the web elements with the provided 'element_type' tag. 
        This method will search in the 'element' if provided, or in 
        the whole web page if not. It will look for elements only on
        the first level y 'only_first_level' is True, or in any level
        if False.

        If 'only_first_level' is True, this will look only in the 
        first child level, horizontally, so a child of a child tag
        won't be returned.
        """
        if not element_type:
            raise Exception('No "element_type" provided.')
        
        object = self.driver
        if element:
            object = element

        if only_first_level:
            # This will only look on first children horizontally
            return object.find_elements(By.XPATH, './' + element_type)
                                         
        return object.find_elements(By.TAG_NAME, element_type)
    
    def find_element_by_xpath_waiting(self, xpath: str, time: int = 30):
        """
        Waits until the WebElement corresponding to the provided 'xpath'
        is visible and returns it if it becomes visible in the 'time' 
        seconds of waiting. It returns None if not.
        """
        return self.__find_element_by_waiting(By.XPATH, xpath, time)
    
    def __find_element_by_waiting(self, by: By, by_value: str, time: int = 30):
        """
        Internal method to simplify the waiting for element until visible
        code reusability.
        """
        wait = WebDriverWait(self.driver, time)
        element = wait.until(EC.visibility_of_element_located((by, by_value)))

        if not element:
            return None
        
        return element
    
    # TODO: When an element is hidden and you cannot interact you
    # can change the style.display
    # driver.execute_script("arguments[0].style.display = 'block';", field)

    def set_file_input(self, element: WebElement, abspath: str):
        """
        Sends the file to a 'type=file' input web element. The 
        provided 'abspath' must be the absolute path to the file
        you want to send.
        """
        if not element:
            raise Exception('No file input "element" provided.')
        
        if not abspath:
            raise Exception('No file "abspath" provided.')
        
        # TODO: Check that it is a valid abspath

        element.send_keys(abspath)
    
    def get_current_page_y_offset(self):
        """
        Returns the current page Y axis offset by executing the
        'return window.pageYOffset' script. This means the amount
        of pixels moved from the origin (top). An offset of 50 
        pixels means that has been a scroll down of 50 pixels.
        The minimum value is 0 when on top of the web page.
        """
        return self.driver.execute_script("return window.pageYOffset")

    def scroll_down(self, pixels: int):
        """
        Scrolls down the web page the amount of 'pixels' provided
        as parameter from the current position. This method will
        make a passive waiting until the new position is reached.
        """
        # TODO: Check if 'pixels' is valid

        pixels = abs(pixels)
        pixels += self.get_current_page_y_offset()

        self.driver.execute_script('window.scrollTo(0, ' + str(pixels) + ')')

        # We wait until movement is completed
        waiting_times = 300
        while (self.get_current_page_y_offset() != pixels and waiting_times > 0):
            self.wait(0.1)
            waiting_times -= 1

    def scroll_up(self, pixels: int):
        """
        Scrolls up the web page the amount of 'pixels' provided
        as parameter from the current position. This method will
        make a passive waiting until the new position is reached.
        """
        # TODO: Check if 'pixels' is valid

        pixels = abs(pixels)
        current_y = self.get_current_page_y_offset()
        if current_y - pixels > 0:
            pixels = current_y - pixels
        else:
            pixels = 0

        self.driver.execute_script('window.scrollTo(0, ' + str(pixels) + ')')

        waiting_times = 300
        while (self.get_current_page_y_offset() != pixels and waiting_times > 0):
            self.wait(0.1)
            waiting_times -= 1

    def scroll_to_element(self, element: WebElement):
        """
        This method scrolls to 50 pixels above the web element
        to make sure it is on the middle of the web page. This
        is very useful to take screenshots. This method will
        make a passive waiting until the new position is 
        reached.
        """
        element_y = element.location['y']
        y = 0

        if element_y > 50:
            y = element_y - 50

        self.execute_script('window.scrollTo(0, ' + str(y) + ')')

        # We wait until movement is completed
        waiting_times = 300
        while (self.get_current_page_y_offset() != y and waiting_times > 0):
            self.wait(0.1)
            waiting_times -= 1

    def get_page_height(self):
        """
        Returns the current page height by executing the
        'return document.body.scrollHeight' script. This means
        the amount of pixels from top to bottom.
        """
        return self.driver.execute_script("return document.body.scrollHeight")

    def screenshot(self, output_filename: str = None):
        """
        Takes a screenshot of the whole page and returns the 
        it as binary data if no 'output_filename' provided. 
        If 'output_filename' is provided, it will be stored 
        locally with that name.
        """
        # TODO: Make this method return the image as binary
        # data always and store if 'output_filename' is 
        # provided, but you cannot do the 'save_screenshot'
        # twice because the webpage can change in the time
        # elapsed between both screenshots.
        if not output_filename:
            return self.driver.get_screenshot_as_png()
        
        self.driver.save_screenshot(output_filename)

        return output_filename
    
    def screenshot_element(self, element: WebElement, output_filename: str = None):
        """
        Takes a screenshot of the provided 'element', that
        means that only the area occupied by that element
        is shown in the screenshot, and returns it as 
        binary data if no 'output_filename' provided or
        will be stored locally if provided.

        Any element of the web page that is over the 
        element will appear in the screenshot blocking it.

        This method will return the 'output_filename' if it
        was provided, so the file has been stored locally,
        or a dict containing 'size' (width, height) and 
        'data' fields.
        """
        # TODO: Make this method return the image as binary
        # data always and store if 'output_filename' is 
        # provided, but you cannot do the 'save_screenshot'
        # twice because the webpage can change in the time
        # elapsed between both screenshots.
        if not element:
            raise Exception('No "element" provided.')
        
        if not output_filename:
            return element.screenshot_as_png
        
        element.screenshot(output_filename)

        return output_filename

    def screenshot_web_page(self, url: str):
        """
        This method will take screenshots of the whole
        web page. It will do in the current page if
        no 'url' is provided, or will navigate to the
        provided 'url' and do it in that one.
        """
        if url:
            self.go_to_web_and_wait_util_loaded(url)

        # TODO: Screenshot the whole page
        FPS = 60
        # Maybe this should be a parameter
        # TODO: We want to make screenshots for a video
        # so depending on 'duration' it will be slower
        # or more dynamic. This method need testing
        duration = 5

        # TODO: Maybe we want to scroll more, or maybe
        # we should pass this a parameter to make it
        # more customizable
        page_height = self.get_page_height()
        if page_height > 1000:
            page_height = 1000

        screenshots = []
        number_of_screenshots = int(duration * FPS)
        window_size = self.driver.get_window_size()

        # TODO: How much should we scroll?
        new_height = 0
        for i in range(number_of_screenshots):
            screenshots.append(self.driver.get_screenshot_as_png())
            height = self.get_current_page_y_offset()
            new_height += page_height / number_of_screenshots
            # We scroll down the difference
            self.scroll_down(new_height - height)

        # TODO: What if we end before

        return screenshots

    def execute_script(self, script: str, *args):
        """
        Executes the provided 'script' synchronously.
        """
        if not script:
            raise Exception('No "script" provided.')
        
        self.driver.execute_script(script, *args)

    def remove_element(self, element: WebElement):
        # TODO: Document
        if not element:
            raise Exception('No "element" provided.')
        
        self.execute_script('arguments[0].remove()', element)
    
    def set_element_width(self, element: WebElement, width: int):
        # TODO: Document
        if not element:
            raise Exception('No "element" provided.')
        
        if not width:
            raise Exception('No "width" provided.')
        
        if width < 0:
            raise Exception('Parameter "width" must be greater than 0.')
        
        # TODO: Do more checkings (is width number and int?)
        
        self.execute_script('arguments[0].style = "width: ' + str(width) + 'px;"', element)

    def set_element_style(self, element: WebElement, style: str):
        # TODO: Document
        if not element:
            raise Exception('No "element" provided.')
        
        if not style:
            raise Exception('No "style" provided.')
        
        self.execute_script('arguments[0].style = "' + style + '"', element)

    def set_element_attribute(self, element: WebElement, attribute: str, value: str):
        # TODO: Document
        if not element:
            raise Exception('No "element" provided.')
        
        if not attribute:
            raise Exception('No "attribute" provided.')
        
        if not value:
            raise Exception('No "value" provided.')
        
        self.execute_script('arguments[0].setAttribute("' + attribute + '", "' + value + '")', element)

    def set_element_inner_text(self, element: WebElement, inner_text: str):
        """
        Sets the provided 'inner_text' in the also provided 'element'
        by applying the script 'element.innerText = "inner_text";'.
        """
        if not element:
            raise Exception('No "element" provided.')
        
        if not inner_text:
            raise Exception('No "inner_text" provided.')

        self.execute_script('arguments[0].innerText = "' + str(inner_text) + '";', element)

    def get_page_size(self):
        """
        Returns a tuple (width, height) containing the
        size of the current web page (attending to the
        screen used).
        """
        size = self.driver.get_window_size()

        return (size['width'], size['height'])
    
    def set_page_size(self, width: int = 1920, height: int = 1080):
        """
        This method resizes the web navigator to the provided
        width and height. It is useful to take screenshots from
        webpages or to validate different screen sizes.
        """
        if not width:
            raise Exception('No "width" provided.')
        
        if not height:
            raise Exception('No "height" provided.')
        
        # TODO: Do more checkings

        self.driver.set_window_size(width, height)

    def add_to_clipboard(self, text: str):
        """
        Adds the provided 'text' to the clipboard to be able to 
        paste it. This method will create a 'textarea' element,
        write the provided 'text' and copy it to the web
        scrapper clipboard.
        """
        TEXT_AREA_ID = 'textarea_to_copy_912312' # a random one
        # I create a new element to put the text, copy it and be able to paste
        js_code = "var p = document.createElement('textarea'); p.setAttribute('id', '" + TEXT_AREA_ID + "'); p.value = '" + text + "'; document.getElementsByTagName('body')[0].appendChild(p);"
        self.execute_script(js_code)

        # Focus on textarea
        textarea = self.find_element_by_id(TEXT_AREA_ID)
        textarea.click()
        self.press_ctrl_a_on_element(textarea)
        self.press_ctrl_c_on_element(textarea)
        # TODO: I can use 'textarea.send_keys(Keys.CONTROL, 'c') to copy, validate
        # actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
        # actions.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()

        # Remove the textarea, it is no longer needed
        js_code = "var element = document.getElementById('" + TEXT_AREA_ID + "'); element.parentNode.removeChild(element);"
        # TODO: Update this with the new version
        self.execute_script(js_code)

    # TODO: Maybe automate some 'execute_javascript' to change
    # 'innerHTML' and that stuff (?)



# TODO: Remove all this below when all refactored
    


def download_fake_call_image(name, output_filename):
    # TODO: Move this to the faker
    URL = 'https://prankshit.com/fake-iphone-call.php'

    try:
        driver = start_chrome()
        go_to_and_wait_loaded(driver, URL)

        inputs = driver.find_elements(By.TAG_NAME, 'input')
        name_textarea = driver.find_element(By.TAG_NAME, 'textarea')

        #operator_input = inputs[4]
        #hour_input = inputs[5]

        name_textarea.clear()
        name_textarea.send_keys(name)

        image = driver.find_element(By.XPATH, '//div[contains(@class, "modal-content tiktok-body")]')
        image.screenshot(output_filename)
    finally:
        driver.close()

# Other fake generators (https://fakeinfo.net/fake-twitter-chat-generator) ad (https://prankshit.com/fake-whatsapp-chat-generator.php)
def download_discord_message_image(text, output_filename):
    URL = 'https://message.style/app/editor'

    try:
        driver = start_chrome()
        go_to_and_wait_loaded(driver, URL)
        
        time.sleep(3)

        clear_embed_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear Embeds')]")
        clear_embed_button.click()

        time.sleep(3)

        input_elements = driver.find_elements(By.TAG_NAME, 'input')
        username_input = input_elements[3]
        avatar_url_input = input_elements[4]

        username_input.clear()
        username_input.send_keys('botsito')

        avatar_url_input.clear()
        avatar_url_input.send_keys('https://cdn.pixabay.com/photo/2016/11/18/23/38/child-1837375_640.png')

        textarea_input = driver.find_element(By.TAG_NAME, 'textarea')
        textarea_input.clear()
        textarea_input.send_keys(text)

        time.sleep(3)

        # get element div class='discord-message'
        discord_message = driver.find_element(By.XPATH, "//div[contains(@class, 'discord-message')]")
        discord_message.screenshot(output_filename)
    finally:
        driver.close()



def test_download_piano_music():
    # TODO: End this, to make it download music generated by this AI
    try:
        options = Options()
        #option_arguments = ['--start-maximized', '--headless=new']
        option_arguments = ['--start-maximized']
        for argument in option_arguments:
            options.add_argument(argument)

        driver = webdriver.Chrome(options = options)
        driver.get('https://huggingface.co/spaces/mrfakename/rwkv-music')
        wait = WebDriverWait(driver, 30)
        download_button_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid=\"checkbox\"]')))

        time.sleep(5)
        actions = ActionChains(driver)
        for i in range(11):
            actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(Keys.SPACE)
        actions.perform()

        input_number_element = driver.find_elements_by_xpath('//*[@data-testid="number-input"]')[0]
        input_number_element.send_keys(14286)

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.perform()

        time.sleep(1)

        driver.execute_script('window.scrollTo(0, 1000)')

        time.sleep(4)

        download_button_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@title=\"Download\"]')))
        #download_button_element = driver.find_elements_by_xpath('//*[@title="Download"]')[0]
        download_button_element.click()

    finally:
        driver.close()


# TODO: Move this method below to the main class
def get_redicted_url(url, expected_url = None, wait_time = 5):
    """
    Navigates to the provided url and waits for a redirection. This method will wait
    until the 'expected_url' is contained in the new url (if 'expected_url' parameter
    is provided), or waits 'wait_time' seonds to return the current_url after that.
    """
    redirected_url = ''

    try:
        options = Options()
        options.add_argument("--start-maximized")
        # Remove this line below for debug
        options.add_argument("--headless=new") # for Chrome >= 109
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        if not expected_url:
            time.sleep(wait_time)
        else:
            wait.until(EC.url_contains(expected_url))

        redirected_url = driver.current_url
    finally:
        driver.close()

    return redirected_url


def get_youtube_summary(video_id):
    """
    Searchs into 'summarize.tech' web to obtain the summary of the video with the 
    provided 'video_id'. This method returns the summary in English, as it is 
    provided by that website.
    """
    url = 'https://www.summarize.tech/www.youtube.com/watch?v=' + video_id

    try:
        options = Options()
        options.add_argument("--start-maximized")
        # Remove this line below for debug
        options.add_argument("--headless=new") # for Chrome >= 109
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        summary = driver.find_element_by_tag_name('section').find_element_by_tag_name('p').get_attribute('innerText')
    finally:
        driver.close()

    return summary

def google_translate(text, input_language = 'en', output_language = 'es'):
    url = 'https://translate.google.com/?hl=es'
    """
    https://translate.google.com/?hl=es&sl=en&tl=es&text=Aporta%20una%20unidad%20de%20traducci%C3%B3n%20(segmento%20y%20traducci%C3%B3n)%20en%20alg%C3%BAn%20par%20de%20idiomas%20a%20MyMemory.%0ASin%20especificar%20ning%C3%BAn%20par%C3%A1metro%20clave%2C%20la%20contribuci%C3%B3n%20est%C3%A1%20disponible%20para%20todos%20(%C2%A1Gracias!).&op=translate

    https://translate.google.com/?hl=es&tab=TT&sl=en&tl=es&op=translate

    https://translate.google.com/?hl=es&tab=TT&sl=en&tl=es&text=La%20%C3%BAnica%20forma%20de%20saberlo%20es%20lo%20que%20t%C3%BA%20digas&op=translate
    """

    url = 'https://translate.google.com/?hl=' + output_language + '&tab=TT&sl=' + input_language + '&tl=' + output_language + '&text=' + text + '&op=translate'

    translation = ''

    # TODO: Verify that this below is working
    driver = ChromeScrapper()
    driver.go_to_web_and_wait_util_loaded(url)
    translation = driver.find_element_by_xpath_waiting('//*[@jscontroller="JLEx7e"]', 10).get_attribute('innerText')
    # TODO: Maybe make a method to obtain the inner text from a WebElement (?)
    return translation

    # TODO: Refactor this as we have a better chrome driver lib now
    try:
        options = Options()
        options.add_argument("--start-maximized")
        # Comment this line below for debug (enables GUI)
        options.add_argument("--headless=new") # for Chrome >= 109
        driver = webdriver.Chrome(options = options)
        driver.get(url)

        tries = 0
        while True:
            if tries < 20:
                try:
                    # We try until it doesn't fail (so we have the text)
                    # TODO: This 'jscontroller' changes from time to time, pay atention
                    translation = driver.find_elements('xpath', '//*[@jscontroller="JLEx7e"]')[0].get_attribute('innerText')
                    tries = 20
                except Exception as e:
                    # TODO: Uncomment this to see if code error or scrapper error
                    #print(e)
                    tries += 1
                    time.sleep(0.250)
            else:
                break
    finally:
        driver.close()

    return translation

    """
    # Intersting options: https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1726
    # Also this: https://stackoverflow.com/questions/19211006/how-to-enable-cookies-in-chromedriver-with-webdriver
    # What about this: options.AddUserProfilePreference("profile.cookie_controls_mode", 0);
    """