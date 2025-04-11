import os
import csv
import logging

import pandas as pd


def save_to_csv(data, filename='vacancies.csv'):
    '''Сохраняет список словарей в CSV-файл'''
    file_exists = os.path.exists(filename)  # Проверяет, существует ли файл "vacancies.csv".
    write_header = not file_exists or os.stat(filename).st_size == 0

    if not data:
        logging.warning('Нет данных для сохранения')
        return
    keys = data[0].keys()  # Заголовки колонок (названия ключей словарей) берет 1й элемент списка

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        if write_header:
            writer.writeheader()  # Записываем заголовки
        writer.writerows(data)  # Записываем все строки

        logging.info(f"Данные сохранены в {filename}")


def load_from_csv(filename='vacancies.csv'):
    '''Загружает CSV-файл в DataFrame'''
    try:
        df = pd.read_csv(filename)
        logging.info(f"Файл загружен: {len(df)} вакансий найдено")
        return df
    except Exception as e:
        logging.error(f"Ошибка при чтении файла: {e}")
        return None
