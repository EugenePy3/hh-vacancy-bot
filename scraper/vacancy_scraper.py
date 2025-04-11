import logging
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_text_or_default(driver, css_selector, default='не указано'):
    """Возвращает текст элемента по CSS-селектору или значение по умолчанию, если элемент не найден."""
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        return element.text.strip()
    except Exception:
        logging.warning(f'Не удалось получить данные для селектора: {css_selector}')
        return default


def parse_vacancy(driver, url, auth):
    """Функция переходит по ссылке и извлекает данные (название, зарплата, описание, опыт и др.)."""

    try:
        driver.get(url)  # Открываем страницу вакансии
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
        )  # Ждем, пока появится заголовок вакансии

        # Извлекаем основные данные
        title = get_text_or_default(driver, '[data-qa="vacancy-title"]')
        salary = get_text_or_default(driver, '[data-qa="vacancy-salary-compensation-type-net"]')
        experience = get_text_or_default(driver, '[data-qa="vacancy-experience"]')
        common_employment = get_text_or_default(driver, '[data-qa="common-employment-text"]')
        works_schedule = get_text_or_default(driver, '[data-qa="work-schedule-by-days-text"]')
        working_hours = get_text_or_default(driver, '[data-qa="working-hours-text"]')
        work_formats = get_text_or_default(driver, '[data-qa="work-formats-text"]')
        description = get_text_or_default(driver, '[data-qa="vacancy-description"]')

        # Значения по умолчанию
        response_link = 'Ссылка на отклик вакансии не найдена.'
        phone_number = 'телефон не указан'
        email_contact = 'email не указан'

        if auth.is_authenticated:  # Проверяем, авторизованы ли мы
            # logging.info(f'Авторизован: {auth.is_authenticated}')

            # Ищем ссылку на отклик
            response_element = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-response-link-top"]')
            if response_element:
                logging.info('Ссылка на отклик найдена')
                response_link = response_element[0].get_attribute("href")
            else:
                logging.info("Ссылка на отклик отсутствует.")

            # Проверяем наличие кнопки контактов
            contact_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                   '[data-qa="show-employer-contacts '
                                                   'show-employer-contacts_top-button"]')
            if contact_buttons:
                logging.info("Кнопка контактов найдена")
                try:
                    # contact_button.click() так почему-то не работает) только клик через js
                    driver.execute_script("arguments[0].click();", contact_buttons[0])
                    logging.info("Клик по контактам выполнен ")
                    # driver.save_screenshot("headless_contacts_debug.png") че-то скриншотил)

                    # Ждём появления блока контактов
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '[data-qa="vacancy-contacts-drop__phone-card"]'))
                    )
                    logging.info('карточка с данными успешно загружена, собираем контакты')

                    # Собираем телефоны
                    phone_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="tel:"]')
                    logging.info(f'найденно: {len(phone_elements)}  телефонов.)')
                    if phone_elements:
                        phone_number = phone_elements[0].get_attribute('href').replace('tel:', '').strip()
                        logging.info(f'Телефон: {phone_number}')
                    else:
                        logging.info('Телефон не найден')

                    # Собираем email
                    email_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
                    logging.info(f'Найдено {len(email_elements)} email-адресов.')
                    if email_elements:
                        email_contact = email_elements[0].get_attribute('href').replace('mailto:', '').strip()
                        logging.info(f'Email: {email_contact}')
                    else:
                        logging.info('Email не найден')

                    # Проверка на полное отсутствие
                    if not phone_elements and not email_elements:
                        logging.info("Контакты отсутствуют полностью (телефон и email)")

                except Exception as e:
                    logging.warning(f"Не удалось получить контакты: {str(e).splitlines()[0]}")

        # Обрабатываем дату публикации
        month_mapping = {
            "января": "January", "февраля": "February", "марта": "March",
            "апреля": "April", "мая": "May", "июня": "June",
            "июля": "July", "августа": "August", "сентября": "September",
            "октября": "October", "ноября": "November", "декабря": "December"
        }

        vacancy_creation_time = get_text_or_default(driver, '.vacancy-creation-time-redesigned span')
        date = 'не указана'  # Значение по умолчанию

        if vacancy_creation_time and vacancy_creation_time != 'не указана':
            parts = vacancy_creation_time.split()
            if len(parts) == 3:
                day, month, year = parts
                month = month_mapping.get(month, "January")  # Подстраховка
                try:
                    date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").date()
                except ValueError as e:
                    logging.warning(f'Ошибка при разборе даты "{vacancy_creation_time}" ({url}): {e}')
            else:
                logging.warning(f'Неожиданный формат даты: {vacancy_creation_time} ({url})')

        logging.info(f'Обработана вакансия: Заголовок {title}, Зарплата: {salary}, Опыт: {experience}, '
                     f'Общая занятость: {common_employment}, График: {works_schedule}, '
                     f'Рабочие часы: {working_hours}, Формат работы: {work_formats}, '
                     f'Дата публикации: {date}, Телефон:  {phone_number}, '
                     f'Email: {email_contact}, Откликнуться на вакансию: {response_link} .')

        return {
            'title': title,
            'salary': salary,
            'experience': experience,
            'common_employment': common_employment,
            'works_schedule': works_schedule,
            'working_hours': working_hours,
            'work_formats': work_formats,
            'description': description,
            'date': date,
            'url': url,
            'response_link': response_link,
            'phone_number': phone_number,
            'email_contact': email_contact,
        }

    except TimeoutException:
        logging.error(f'Ошибка: страница вакансии {url} долго не загружается')
    except Exception as e:
        logging.error(f'Ошибка при обработке вакансии {url}: {e}')

    return None
