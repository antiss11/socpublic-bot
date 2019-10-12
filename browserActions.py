from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver import ActionChains
import pickle


class BrowserCore:

    def __init__(self, *options):
        if options:
            option = webdriver.ChromeOptions()
            for i in options:
                option.add_argument(i)
            self.browser = webdriver.Chrome(options=option,
                                            service_log_path='NUL')
        else:
            self.browser = webdriver.Chrome()

    def save_cookies(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.browser.get_cookies(), filehandler)

    def load_cookies(self, path):
        with open(path, 'rb') as cookies_file:
            cookies = pickle.load(cookies_file)
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.browser.add_cookie(cookie)

    def close(self):
        for i in range(self.tabs_number()):
            self.switch_window(0)
            self.browser.close()

    def close_tab(self):
        self.browser.close()

    def execute_script(self, script, elem):
        self.browser.execute_script(script, elem)

    def fill_form(self, text, form_id=None, xpath=None, el_class=None, css=None):
        if form_id:
            self.browser.find_element_by_id(form_id).send_keys(text)
        elif xpath:
            self.browser.find_element_by_xpath(xpath).send_keys(text)
        elif el_class:
            self.browser.find_element_by_class_name(el_class).send_keys(text)
        elif css:
            self.browser.find_element_by_css_selector(css).send_keys(text)

    def find_element(self, xpath=None, text=None, css=None, id=None, link_text=None, all=None):
        if xpath:
            if all:
                return self.browser.find_elements_by_xpath(xpath)
            elif not all:
                return self.browser.find_element_by_xpath(xpath)
        if text:
            if all:
                return self.browser.find_elements_by_link_text(text)
            elif not all:
                return self.browser.find_element_by_link_text(text)
        if css:
            if all:
                return self.browser.find_elements_by_css_selector(css)
            elif not all:
                return self.browser.find_element_by_css_selector(css)
        if id:
            return self.browser.find_element_by_id(id)
        if link_text:
            return self.browser.find_element_by_link_text(link_text)

    def get_page(self, url):
        self.browser.get(url)

    def set_position(self):
        self.browser.set_window_position(-1500, 0)

    def get_current_url(self):
        return self.browser.current_url

    def get_current_page_source(self):
        return self.browser.page_source

    def new_tab(self):
        self.browser.execute_script('''window.open("","_blank");''')

    def scroll_down(self, count=None):
        if count:
            for i in range(0, count):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
        else:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def switch_default_content(self):
        self.browser.switch_to.default_content()

    def switch_frame(self, frame_name):
        self.browser.switch_to.frame(frame_name)

    def scroll_to_element(self, element):
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def switch_window(self, number):
        handles = self.browser.window_handles
        self.browser.switch_to.window(handles[number])

    def set_size(self, max=None, min=None):
        if max:
            self.browser.set_window_size(1920, 1080)
        elif min:
            self.browser.minimize_window()

    def take_screenshot(self, filename):
        self.browser.save_screenshot(filename)

    def waiting(self, xpath=None, id=None, elem_class=None, link_text=None,
                type=None, delay=None):
        delay = delay or 20

        if type == "default":
            if xpath:
                 WebDriverWait(self.browser, delay).until(
                     EC.presence_of_element_located((By.XPATH, xpath)))
            elif id:
                WebDriverWait(self.browser, delay).until(
                    EC.presence_of_element_located((By.ID, id)))
            elif elem_class:
                WebDriverWait(self.browser, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, elem_class)))
            elif link_text:
                WebDriverWait(self.browser, delay).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text)))

        elif type == "element_to_be_clickable":
            if xpath:
                 WebDriverWait(self.browser, delay).until(
                     EC.element_to_be_clickable((By.XPATH, xpath)))
            elif id:
                WebDriverWait(self.browser, delay).until(
                    EC.element_to_be_clickable((By.ID, id)))
            elif elem_class:
                WebDriverWait(self.browser, delay).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, elem_class)))
            elif link_text:
                WebDriverWait(self.browser, delay).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, link_text)))

    def get_title(self):
        return self.browser.title

    def tabs_number(self):
        return len(self.browser.window_handles)

    def move_cursor(self, element):
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()

    def kill_extra_tabs(self):
        for i in range(self.tabs_number() - 1):
            self.close()

    def alert_check(self):
        try:
            self.browser.switch_to.alert
            return True
        except NoAlertPresentException:
            return False
