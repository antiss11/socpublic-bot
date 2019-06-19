from lxml import html
from selenium import webdriver
import time
from lxml.etree import tostring
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,\
        NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains

VK_PAGE = "https://vk.com/"
VK_PEOPLE = "https://vk.com/search?c%5Bper_page%5D=40&c%5Bsection%5D=people"
VK_GROUPS = "https://vk.com/groups"



VK_ID_LOGIN_BUTTON = "index_login_button"
VK_ID_LOGIN_LOGIN = "index_email"
VK_ID_LOGIN_PASSWORD = "index_pass"
VK_XPATH_WAITING_FORM = "//span[@class='left_label inl_bl']"
VK_ID_SEARCH_FORM = "search_query"
VK_ID_PEOPLE_NUMBER = "page_block_header_count"
VK_XPATH_WAITING_PEOPLE = "//button[contains(@id, 'search')]"
VK_XPATH_AVATAR = "//img[@class='search_item_img']/@src"
VK_XPATH_PEOPLE_DIVS = "//div[@class='people_row search_row clear_fix']"
VK_XPATH_MAN_URL = "//a[@class='search_item_img_link _online']/@href"
VK_XPATH_POPUP_LOGIN = "//input[@name='email']"
VK_XPATH_POPUP_PASSWORD = "//input[@name='pass']"
VK_XPATH_LIKE_BUTTON = "//div[@class='like_button_icon']"
VK_XPATH_POPUP_LOGIN_BUTTON = "//button[@id='install_allow']"
VK_XPATH_ADD_FRIEND_BUTTON = "//button[@class='flat_button button_wide']"
VK_XPATH_JOIN_GROUP_BUTTON = "//button[@class='flat_button button_wide']"
VK_XPATH_POPUP_CAPCHA = "//div[@class='popup_box_container']"
VK_XPATH_LIKED = "//a[@class='like_btn like _like active']"
VK_XPATH_GROUPS = "//a[@class='group_row_title']"
VK_XPATH_LIKE_BLOCK = "//a[@class='like_btn like _like']"
VK_XPATH_LIKE_BLOCK_COUNT = "//div[@class='like_button_count']"
VK_XPATH_POST = "//div[@class='post_info']"
VK_XPATH_POST_DATE = "//a[@class='post_link']"
VK_CSS_POST = ".post_info"
VK_CSS_LIKED = ".like_btn.like.active"
VK_CSS_LIKES_NUMBER = ".like_button_count"
VK_XPATH_POST_BLOCK = "//div[@class='_post post page_block all own post--with-likes deep_active']"
VK_CSS_POPUP_LOGIN = "input.oauth_form_input:nth-child(7)"
VK_XPATH_JOIN_GROUP_BUTTON = "//*[@id='join_button']"
VK_XPATH_SUBSCRIBE_BUTTON  = "//*[@id='public_subscribe']"
VK_XPATH_JOINED_GROUP = "//span/text()[contains(.,'Вы участник')]"
VK_XPATH_LEFT_MENU_ELEMENT = "//span[@class='left_label inl_bl']"


class BrowserCore:

    def __init__(self, *options):
        if options:
            option = webdriver.ChromeOptions()
            for i in options:
                option.add_argument(i)
            self.browser = webdriver.Chrome(options=option)
        else:
            self.browser = webdriver.Chrome()

    def click(self, id=None, xpath=None, key=None):
        if id is not None and key is None:
            self.browser.find_element_by_id(id).click()
        elif id is not None and key is not None:
            self.browser.find_element_by_id(id).send_keys(key)
            self.browser.find_element_by_id(id).click()
        elif xpath is not None and key is None:
            self.browser.find_element_by_xpath(xpath).click()
        elif xpath is not None and key is not None:
            self.browser.find_element_by_xpath(xpath).send_keys()
            self.browser.find_element_by_xpath(xpath).click()

    def close(self):
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

    def find_element(self, xpath=None, text=None, css=None, id=None, all=None):
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

    def get_page(self, url):
        self.browser.get(url)

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

    def take_screenshot(self, filename):
        self.browser.save_screenshot(filename)

    def waiting(self, xpath=None, id=None, elem_class=None, delay=None):
        delay = delay or 20
        try:
            if xpath is not None:
                 WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            elif id is not None:
                WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.ID, id)))
            elif elem_class is not None:
                WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, elem_class)))
        except TimeoutException:
            pass

    def get_title(self):
        return self.browser.title

    def tabs_number(self):
        return len(self.browser.window_handles)

    def skip_warning(self):
        try:
            self.browser.switch_to.alert.accept()
        except Exception:
            pass


class VkActions(BrowserCore):

    def vk_popup_login(self, login, password):
        try:
            self.waiting(xpath=VK_XPATH_POPUP_LOGIN, delay=5)
            self.fill_form(login, xpath=VK_XPATH_POPUP_LOGIN)
            self.fill_form(password, xpath=VK_XPATH_POPUP_PASSWORD)
            self.click(xpath=VK_XPATH_POPUP_LOGIN_BUTTON)
        except AttributeError:
            pass

    def vk_login(self, login, password):
        self.fill_form(login, form_id=VK_ID_LOGIN_LOGIN)
        self.fill_form(password, form_id=VK_ID_LOGIN_PASSWORD)
        self.click(id=VK_ID_LOGIN_BUTTON)

    def vk_add_friend(self):
        self.find_element(xpath=VK_XPATH_ADD_FRIEND_BUTTON).click()

    def vk_add_like(self, element=False):
        if element:
            element.find_element_by_xpath(xpath=VK_XPATH_LIKE_BUTTON).click()
        elif not element:
            self.find_element(xpath=VK_XPATH_LIKE_BUTTON).click()

    def vk_check_liked(self, elem=None):
        try:
            if elem:
                elem.find_element_by_css_selector(VK_CSS_LIKED)
                return True
            else:
                self.find_element(xpath=VK_XPATH_LIKED)
        except NoSuchElementException:
            return False

    def join_group(self):
        try:
            self.find_element(xpath=VK_XPATH_JOIN_GROUP_BUTTON).click()
        except NoSuchElementException:
            self.find_element(xpath=VK_XPATH_SUBSCRIBE_BUTTON).click()


    def vk_check_joined_group(self):
        try:
            self.find_element(xpath=VK_XPATH_JOINED_GROUP)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def vk_post_date(post):
        date = post.find_element_by_xpath(VK_XPATH_POST_DATE).text
        return date

    @staticmethod
    def vk_likes_number(post):
        likes = post.find_element_by_css_selector(VK_CSS_LIKES_NUMBER).text
        return int(likes)




def parse_by_xpath(html_code, xpath):
    tree = html.fromstring(html_code)
    return tree.xpath(xpath)


def html_to_string(html_code):
    return html.fromstring(tostring(html_code))


def vk_confirm_popup_check(browser):
    try:
        browser.find_element(xpath=VK_XPATH_POPUP_CAPCHA)
        return True
    except NoSuchElementException:
        return False


def check502(browser):
    try:
        browser.find_element(text="502 Bad Gateway")
        return True
    except NoSuchElementException:
        return False


