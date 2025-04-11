import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def test_search_input(driver):
    """Проверяет, что поле поиска корректно принимает введенный текст 'Python разработчик'."""
    input_job_search = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )
    input_job_search.send_keys('Python разработчик')

    # Проверяем, что в поле действительно появился введенный текст
    assert input_job_search.get_attribute('value') == 'Python разработчик'


def test_modal_close(driver):
    """Проверяет, что модальное окно закрывается, если оно появляется."""
    try:
        modal_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.bloko-modal-close-button'))
        )
        modal_close.click()

        # Проверяем, что модальное окно действительно исчезло
        with pytest.raises(TimeoutException):
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.bloko-modal-close-button'))
            )
    except TimeoutException:
        pass  # Если модального окна нет, тест продолжается






