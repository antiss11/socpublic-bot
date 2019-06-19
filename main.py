from main import BrowserCore, VkActions
from selenium.common.exceptions import NoSuchElementException
import random
import time
import datetime


VK_LOGIN = ""
VK_PASSWORD = ""


VK_PASSWORD = ""
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"


SOCPUBLIC_PAGE = "https://socpublic.com/"
SOCPUBLIC_XPATH_LOGIN_BUTTON = "/html/body/div[1]/div/div[2]/ul/li[8]/a"
SOCPUBLIC_XPATH_VK_BUTTON = "//*[@id='uLogin']/div/div[1]"
SOCPUBLIC_TASKS_TIMER = "http://socpublic.com/account/visit.html?type=frame"
SOCPUBLIC_XPATH_TASK = "//a[@title='Смотреть сайт']"
SOCPUBLIC_TASKS_WITHOUT_TIMER = "http://socpublic.com/account/visit.html?type=redirect"
SOCPUBLIC_XPATH_CAPTCHA_BUTTON_1 = "//button[@class='btn btn-default var0']"
SOCPUBLIC_XPATH_CAPTCHA_BUTTON_2 = "//button[@class='btn btn-default var1']"
SOCPUBLIC_XPATH_CAPTCHA_BUTTON_3 = "//button[@class='btn btn-default var2']"
SOCPUBLIC_XPATH_CAPTCHA_BUTTON_4 = "//button[@class='btn btn-default var3']"
SOCPUBLIC_ID_CAPTCHA_FRAME = "counter_frame"
SOCPUBLIC_XPATH_TASK_BOTTOM = "//div[@class='bottom']"
SOCPUBLIC_XPATH_CAPTCHA = "//div[@class='captcha']"
SOCPUBLIC_XPATH_CAPTCHA_SRC = "//div[@class='captcha']/div[@class='img']/img"
SOCPUBLIC_XPATH_BONUS= "/html/body/div[1]/div/div/div[2]/a[2]"
SOCPUBLIC_XPATH_BONUS_LINK = "/html/body/div[3]/div[1]/div[2]/div/div\
            [2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]"
SOCPUBLIC_ID_GET_BONUS_BUTTON = "get_bonus"
SOCPUBLIC_XPATH_BALANCE = "//span[@class='balance_rub']"


class Log:
    def __call__(self, msg):
        time_now = time.strftime("%H:%M:%S_%d/%m")
        if len(msg) > 50:
            msg = msg[0:50] + "..."
        print("{:<40} {:>20}".format(msg, time_now))


class SocpublicController(BrowserCore):
    log = Log()

    def __init__(self, *options):
        BrowserCore.__init__(self, *options)

    def login(self):
        self.get_page(SOCPUBLIC_PAGE)
        self.waiting(xpath=SOCPUBLIC_XPATH_LOGIN_BUTTON)
        self.click(xpath=SOCPUBLIC_XPATH_LOGIN_BUTTON)
        time.sleep(random.randrange(600, 1500) / 1000)
        self.waiting(xpath=SOCPUBLIC_XPATH_VK_BUTTON)
        self.click(xpath=SOCPUBLIC_XPATH_VK_BUTTON)
        self.switch_window(1)
        VkActions.vk_popup_login(self, VK_LOGIN, VK_PASSWORD)
        self.switch_window(0)
        self.log("Login success")

    def is_captcha_frame(self):
        try:
            self.find_element(id=SOCPUBLIC_ID_CAPTCHA_FRAME)
            return True
        except NoSuchElementException:
            return False

    def get_timer_task(self):
        task_bottom_text = self.find_element(xpath=SOCPUBLIC_XPATH_TASK_BOTTOM).text
        return int(task_bottom_text.split(" ")[2])

    def check_captcha_remains(self):
        try:
            self.find_element(id=SOCPUBLIC_ID_CAPTCHA_FRAME)
            return True
        except NoSuchElementException:
            return False

    def captcha_click(self):
        self.find_element(xpath=SOCPUBLIC_XPATH_CAPTCHA_BUTTON_1).click()

    def get_balance(self):
        return self.find_element(xpath=SOCPUBLIC_XPATH_BALANCE).text

    def do_tasks_with_timer(self):
        self.get_page(SOCPUBLIC_TASKS_TIMER)
        self.log(self.get_balance())
        timer = self.get_timer_task()
        self.find_element(xpath=SOCPUBLIC_XPATH_TASK).click()
        time.sleep(timer + random.randrange(600, 1200) / 1000)
        self.do_captcha(timer)

    def do_captcha(self, timer):
        captcha = True
        while captcha:
            self.switch_window(-1)
            self.switch_frame(SOCPUBLIC_ID_CAPTCHA_FRAME)
            self.captcha_click()
            time.sleep(0.5)
            self.switch_window(-1)
            time.sleep(1)
            captcha = self.check_captcha_remains()
            time.sleep(1)
            if captcha is False:
                time.sleep(0.3)
                self.close()
                self.switch_window(0)
            elif captcha:
                time.sleep(timer + random.randrange(600, 1200) / 1000)


def sleep(log=None):
    sleeping_hours = random.randrange(1, 4)
    sleeping_minutes = random.randrange(1, 60)
    sleeping_seconds = random.randrange(1, 60)

    def get_now():
        return datetime.datetime.today()

    now = get_now()

    def time_normalization():
        year = now.year
        month = now.month
        day = now.day
        if sleeping_hours + now.hour > 23:
            hour = sleeping_hours + now.hour - 24
            day += 1
        else:
            hour = sleeping_hours + now.hour
        if sleeping_minutes + now.minute > 59:
            minute = sleeping_minutes + now.minute - 60
        else:
            minute = sleeping_minutes + now.minute
        if sleeping_seconds + now.second > 59:
            second = sleeping_seconds + now.second - 60
        else:
            second = sleeping_seconds + now.second
        return year, month, day, hour, minute, second

    sleeping_end_date = datetime.datetime(*time_normalization())

    if log:
        log("Continue at " + str(sleeping_end_date))

    while now < sleeping_end_date:
        time.sleep(30)
        now = get_now()


def main():
    browser = SocpublicController("--headless",
                                  "--mute-audio",
                                  "--user-agent={0}".format(USER_AGENT))

    browser.login()
    while True:
        try:
            browser.do_tasks_with_timer()
            time.sleep(random.randrange(600, 2000) / 1000)
        except NoSuchElementException:
            sleep(SocpublicController.log)


if __name__ == "__main__":
    main()
