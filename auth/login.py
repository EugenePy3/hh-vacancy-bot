from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import logging
import time


from scraper.config import EMAIL, PASSWORD
from scraper.browser import BASE_URL


class Authenticator:
    LOGIN_URL = f'{BASE_URL}account/login'

    def __init__(self, driver):
        self.driver = driver  # Инициализировали драйвер
        self.is_authenticated = False  # по умолчанию не авторизованы

    def login(self):
        '''пытаемся войти в аккаунт, если есть логин и пароль'''
        if not EMAIL or not PASSWORD:
            logging.info('Переменные окружения не заданы. Работаем без авторизации.')
            return False

        logging.info('Попытка авторизации')
        self.driver.get(self.LOGIN_URL)  # Открываем страницу логина

        try:
            # Ожидаем поле ввода логина
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'login'))
            )

            email_field.send_keys(EMAIL)
            logging.info('логин введен успешно')

            # Кликаем "Войти с паролем"
            enter_with_pass = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="expand-login-by-password-text" ]'))
            )
            enter_with_pass.click()
            logging.info("Клик по 'Войти с паролем' успешен.")

            # Ожидаем поле пароля
            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="login-input-password"]'))
            )
            password_field.send_keys(PASSWORD)
            logging.info('пароль введен успешно')
            password_field.send_keys(Keys.RETURN)
            # time.sleep(15)  # задержка для ввода каптчи

            # Проверяем, что зашли в аккаунт
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="mainmenu_applicantProfile"]'))
            )
            self.is_authenticated = True  # Успешная авторизация
            logging.info("Успешно авторизованы!")
            return True

        except TimeoutException:
            logging.warning('Ошибка авторизации, проверьте логин и пароль')
            return False
