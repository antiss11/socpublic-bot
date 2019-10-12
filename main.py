from browserActions import BrowserCore
from vkActions import VkActions
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import random
import time
import additionalFunctions
import traceback
import sys

VK_LOGIN = ""
VK_PASSWORD = ""
USER_AGENT = ""


class Log:
    """ Объект класса вызывается как функция
    Записывает в консоль время и сообщение в формате [hh:mm:ss] *message*  """
    def __call__(self, msg):
        time_now = time.strftime("%H:%M:%S_%d/%m")
        if len(msg) > 50:
            msg = msg[0:50] + "..."
        print("[{}] {}".format(time_now, msg))


def sleep(wait_time):
    """Ждет время wait_time плюс от 2 до 6 секунд"""
    time.sleep(wait_time + random.randrange(2000, 6000) / 1000)


class SocpublicController(BrowserCore):

    def __init__(self, *options):
        """Инициализация браузера и создание объекта лога и свойства баланса.
        Баланс представлен в виде строки"""
        BrowserCore.__init__(self, *options)
        self.log = Log()
        self.balance = ""

    def login(self):
        """ Логин на сайте через VK """
        self.get_page("https://socpublic.com/")
        self.waiting(link_text='Вход')
        self.find_element(link_text='Вход').click()
        time.sleep(random.randrange(600, 1500) / 1000)
        self.waiting(xpath=VK_LOGIN)
        self.find_element(xpath="//*[@id='uLogin']/div/div[1]").click()
        self.switch_window(1)
        VkActions.popup_login(self, VK_LOGIN, VK_PASSWORD)
        self.switch_window(0)
        try:
            self.find_element(link_text="Приватная зона")
            raise PermissionError("Не залогинились!")
        except NoSuchElementException:
            self.log("Успешный логин")

    def get_timer_task(self):
        """ Функция для получения таймера задания, используется на странице с заданиями.
        Ищет первый таймер на странице """
        task_bottom_text = self.find_element(xpath="//div[@class='bottom']").text
        return int(task_bottom_text.split(" ")[2])

    def check_captcha_remains(self):
        """ Функция-предикат. Проверка наличия капчи на странице задания.
            Используется для проверки правильности нажатия на капчу"""
        try:
            self.find_element(xpath="//div[@class='frame-counter']")
            return True
        except NoSuchElementException:
            return False

    def captcha_click(self):
        """" Функция клика по первой (из 4) кнопок капчи """
        self.find_element(xpath="//button[@class='btn btn-default var0']").click()

    def update_balance(self):
        """ Обновляет свойство balance объекта """
        self.balance = self.find_element(xpath="//span[@class='balance_rub']").text

    def do_tasks_with_timer(self):
        """ Функция-предикает делает задания с таймером.
         Возвращает False, если заданий нет. """
        task_xpath = "//a[@title='Смотреть сайт']"
        self.get_page("https://socpublic.com/account/visit.html?type=frame")
        try:
            self.find_element(xpath=task_xpath)
        except NoSuchElementException:
            return False
        self.update_balance()
        self.log(self.balance)
        timer = self.get_timer_task()
        self.find_element(xpath=task_xpath).click()
        time.sleep(timer + random.randrange(600, 1200) / 1000)
        self.do_captcha(timer)
        return True

    def do_captcha(self, timer):
        """ Бесконечно кликает по первой кнопке капчи, пока check-captcha-remains
         не вернет False. После решения капчи закрывает вкладку и переходит на
         первую вкладку """
        captcha = True
        while captcha:
            self.switch_window(-1)
            time.sleep(1)
            self.captcha_click()
            time.sleep(0.5)
            self.switch_window(-1)
            time.sleep(1)
            captcha = self.check_captcha_remains()
            time.sleep(1)
            if captcha is False:
                time.sleep(0.3)
                self.close_tab()
                self.switch_window(0)
            elif captcha:
                sleep(timer)

    def take_bonus(self):
        """ Функция-предикат берет бонус на главной странице, не совершая перехода на нее.
        Использовать на открытой главной странице. Возвращается False, если бонуса нет. """
        bonus_el_xpath = "//div[@class='font-size-16']"
        try:
            self.find_element(link_text="Бонус").click()
        except NoSuchElementException:
            return False
        while True:
            self.switch_window(-1)
            self.waiting(xpath=bonus_el_xpath)
            self.find_element(xpath=bonus_el_xpath).click()
            self.switch_window(-1)
            time.sleep(12)
            self.captcha_click()
            time.sleep(5)
            self.switch_window(-1)
            try:
                self.find_element(id="get_bonus").click()
                self.log("Бонус взят")
                return True
            except ElementNotInteractableException:
                pass


def main():
    is_next_day = additionalFunctions.is_next_day()
    browser = SocpublicController(
        "--headless",
        "--mute-audio",
        "--user-agent={0}".format(USER_AGENT),
        "--log-level=3",
        "lang=ru"
    )
    browser.set_size(max=True)
    browser.login()
    while True:
        if is_next_day():
            browser.close()
            main()
        else:
            try:
                browser.take_bonus()
            except NoSuchElementException:
                pass
            if browser.do_tasks_with_timer():
                # Если задание сделано
                additionalFunctions.sleep_between()
            else:
                additionalFunctions.waiting_tasks(h_from=0, h_to=1, m_from=0, m_to=30, log=browser.log)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        input('Нажмите Enter для продолжения')