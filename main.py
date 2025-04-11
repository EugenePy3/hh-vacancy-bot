import logging
import asyncio
from datetime import datetime

from auth.login import Authenticator
from scraper.browser import get_driver
from scraper.parser import open_url, get_vacancy_links
from scraper.vacancy_scraper import parse_vacancy

from utils.file_operations import save_to_csv
from utils.ranking import rank_vacancies
from utils.logger import setup_logger
from bot.bot import send_vacancies

if __name__ == '__main__':
    setup_logger()  # Подлючение логирование
    logging.info(f'Скрипт запущен: {datetime.now()}')

    # === Браузер и авторизация ===
    driver = get_driver(headless=True)

    try:
        #  Создаём объект авторизации и пытаемся войти
        auth = Authenticator(driver)
        is_logged_in = auth.login()

        if is_logged_in:
            logging.info("Теперь можно парсить вакансии!")
        else:
            logging.info("Продолжаем без авторизации.")

        # === Получение ссылок на вакансии ===
        open_url(driver, is_logged_in)
        vacancy_links = get_vacancy_links(driver)
        if not vacancy_links:
            logging.warning('Ccылки на вакансию не были получены. Завершаем работу.')

        # === Парсинг вакансий ===
        all_vacancies_data = []  # список для хранения всех вакансий
        for link in vacancy_links:
            data = parse_vacancy(driver, link, auth)
            if data:
                all_vacancies_data.append(data)  # Добавляем данные вакансии в список

        # === Сохранение, ранжирование, отправка в Телеграм-бот ===
        save_to_csv(all_vacancies_data)  # Сохраняем все данные в CSV
        rank_vacancies()  # вызов ранжирования
        asyncio.run(send_vacancies())  # Асинхронный запуск

        logging.info('Скрипт завершён успешно.')

    except Exception as e:
        logging.error(f'Произошла ошибка: {e}')

    finally:
        if driver:
            driver.quit()
            logging.info("Браузер закрыт.")
