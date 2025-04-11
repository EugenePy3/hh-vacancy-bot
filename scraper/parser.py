import time
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from .config import SEARCH_QUERY
from .config import MAX_PAGES


def open_url(driver, is_logged_in):
    '''Функция, которая вводит "Python разработчик" в поиск на hh.ru'''

    try:
        selector = '[data-qa="search-input"]'

        if not is_logged_in:
            logging.info('Ищем кнопку "Поиск"...')
            # Если НЕ авторизован, сначала кликаем "Поиск"
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="supernova-search"]'))
            )
            search_button.click()
            logging.info('Клик по кнопке "Поиск" успешен')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

        input_job_search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )

        input_job_search.send_keys(SEARCH_QUERY)
        logging.info(f'Успешно введено {SEARCH_QUERY}')

        #  нажимаем на Enter
        input_job_search.send_keys(Keys.RETURN)
    except TimeoutException:
        logging.error('поисковое поле не найдено')

    except ElementNotInteractableException:
        logging.error('Поисковое поле найдено, но к нему нельзя обратиться')

    try:
        modal_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.bloko-modal-close-button'))
        )
        modal_close.click()
        logging.info('Всплывающий элемент успешно закрыт')
    except TimeoutException:
        logging.info('Модальное окно не появилось')


def get_vacancy_links(driver):
    '''Собирает ссылки на все вакансии со всех страниц'''
    try:
        all_links = []
        for page in range(1, MAX_PAGES + 1):  # количество страниц
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-qa="pager-page"]'))
            )
            # Собираем ссылки с текущей страницы
            vacancies = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]'))
            )

            links = [vacancy.get_attribute('href') for vacancy in vacancies]
            all_links.extend(links)  # Добавляем ссылки в общий список

            logging.info(f'На странице {page} собрано {len(links)} ссылок на вакансии')

            try:
                # Прокручиваем страницу до низа c помощью js
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Ждём, пока кнопка станет видимой
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[data-qa="pager-page"][aria-current="false"]'))
                )
                next_page_button.click()

                # Теперь ищем кнопку
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-qa="pager-page"][aria-current="false"]'))
                )
                next_page_button.click()
                time.sleep(2)  # Даем время на загрузку следующей страницы
            except TimeoutException:
                logging.error('Не удалось найти кнопку "Следующая страница"')

            # Ожидаем, пока страница обновится
            WebDriverWait(driver, 10).until(EC.staleness_of(vacancies[0]))

            logging.info(f'Всего собрано {len(all_links)} ссылок на вакансии')
        return all_links

    except TimeoutException:
        logging.error('Не удалось найти вакансии')
        return []



