from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from .config import CHROME_DRIVER_PATH
from .config import BASE_URL


def get_driver(headless=False):
    """Создаёт и настраивает экземпляр ChromeDriver"""
    service = Service(CHROME_DRIVER_PATH)
    options = Options()

    # подключение режима без интерфейса
    if headless:
        options.add_argument('--headless=new')

    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    # чтобы headless работал как обычный браузер
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 "
        "Safari/537.36")

    # отключение автоматики, отключение блокировки всплывающих окон, удаляет служебную плашку сверху браузера
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(service=service, options=options)

    # Патч: navigator.webdriver = undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(BASE_URL)
    return driver
