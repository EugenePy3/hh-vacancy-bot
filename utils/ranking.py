import re
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd

from .file_operations import load_from_csv
from scraper.config import (
    SALARY_WEIGHT, SALARY_MAX_SCORE, EXPERIENCE_SCORES, WORK_FORMAT_KEYWORDS, STACK, STACK_SCORE,
    WORK_FORMAT_SCORE, KEYWORDS, KEYWORD_SCORE, JUNIOR_KEYWORDS, JUNIOR_SCORE,
    JUNIOR_TITLES, JUNIOR_TITLE_SCORE, INTERN_TITLES, INTERN_TITLE_SCORE,
    SENIOR_TITLES, SENIOR_PENALTY, NOT_JUNIOR_TITLES, NOT_JUNIOR_PENALTY,
    NOT_JUNIOR_KEYWORDS, NOT_JUNIOR_DESCRIPTION_PENALTY,
    RECENT_VACANCY_BONUS_DAYS, RECENT_VACANCY_BONUS_SCORE
)

# Путь к корневой папке проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Путь к файлам
VACANCIES_CSV = BASE_DIR / 'vacancies.csv'
RANKED_CSV = BASE_DIR / 'ranked_vacancies.csv'


def clean_salary(salary_str):
    """
    Преобразует строку с зарплатой в числовое значение (среднее значение 'от' и 'до').
    """
    if pd.isna(salary_str):
        return 0  # Если зарплата не указана, присваиваем 0
    numbers = list(map(int, re.findall(r'\d+', salary_str.replace(' ', ''))))
    if len(numbers) == 2:  # Если указаны "от" и "до"
        return sum(numbers) / 2
    elif len(numbers) == 1:  # Если указана только одна цифра
        return numbers[0]
    return 0  # Если не удалось определить число


def calculate_score(row):
    """
    Рассчитывает общий балл для вакансии по критериям:
#     - зарплата  (чем выше, тем лучше).
#     - опыт  (меньше требований — лучше).
#     - формат работы  (удалёнка, гибкий график, частичная занятость, проектная работа, совмещение—плюс).
#     - ключевые слова в описании Наличие ключевых слов в описании (Python, Selenium и т.д.).
    """
    score = 0

    # Зарплата (Максимально 30 баллов) (max=30%)
    if row['salary']:
        score += min((clean_salary(row['salary']) / 1000) * SALARY_WEIGHT, SALARY_MAX_SCORE)

    # Опыт (30%) — меньше лет опыта -> больше баллов
    experience_str = row['experience'].lower()  # Приводим текст к нижнему регистру
    for exp_key, exp_score in EXPERIENCE_SCORES.items():
        if exp_key in experience_str:
            score += exp_score
            break

    # Формат работы (20%)
    for word_f in WORK_FORMAT_KEYWORDS:
        if word_f in row['work_formats'].lower():
            score += WORK_FORMAT_SCORE
            break

    # Рабочий стек начинающего
    stack_matches = sum(
        1 for tech in STACK if tech.lower() in row['description'].lower() or tech.lower() in row['title'].lower())
    if stack_matches >= 3:
        score += STACK_SCORE[3]
    elif stack_matches == 2:
        score += STACK_SCORE[2]
    elif stack_matches == 1:
        score += STACK_SCORE[1]

    # Наличие ключевых слов в описании (10%)
    if any(word in row['description'].lower() for word in KEYWORDS):
        score += KEYWORD_SCORE

    # дополнительные ключевые слова для джунов (20%)
    for word in JUNIOR_KEYWORDS:
        if word in row['description'].lower():
            score += JUNIOR_SCORE
            break

    #  Заголовок вакансии - Если в заголовке вакансии есть Junior/Intern - большой бонус
    title_lower = row['title'].lower()
    if any(word in title_lower for word in JUNIOR_TITLES):
        score += JUNIOR_TITLE_SCORE
    if any(word in title_lower for word in INTERN_TITLES):
        score += INTERN_TITLE_SCORE
    if any(word in title_lower for word in SENIOR_TITLES):
        score -= SENIOR_PENALTY
    if any(word in title_lower for word in NOT_JUNIOR_TITLES):
        score -= NOT_JUNIOR_PENALTY

    # Подозрительные описания для Junior
    description_lower = row['description'].lower()
    if any(kw in description_lower for kw in NOT_JUNIOR_KEYWORDS):
        score -= NOT_JUNIOR_DESCRIPTION_PENALTY

    # Недавно опубликованные вакансии
    today = datetime.today().date()
    if isinstance(row['date'], datetime):
        days_diff = (today - row['date']).days
        if days_diff <= RECENT_VACANCY_BONUS_DAYS:
            score += RECENT_VACANCY_BONUS_SCORE

    logging.debug(f"Опыт: {row['experience']}, начислено {score} баллов")
    return max(score, 0)


def rank_vacancies():
    '''Ранжирует вакансии по баллам'''
    df = load_from_csv(VACANCIES_CSV)
    if df is None:
        logging.warning(f'Файл {VACANCIES_CSV} не загружен. Прерываем ранжирование.')
        return None
    if df.empty:
        logging.warning('Файл загружен, но DataFrame пуст. Ранжирование не проводится.')
        return None

    # Добавляем новый столбец 'score' с рассчитанными баллами
    df['score'] = df.apply(calculate_score, axis=1)

    # Сортировка по убыванию баллов
    df_sorted = df.sort_values(by='score', ascending=False)

    # Сохраняем результаты в CSV
    df_sorted.to_csv(RANKED_CSV, index=False)
    logging.info(f"Файл сохранен: {RANKED_CSV}, вакансии отсортированы")

    return df_sorted


if __name__ == "__main__":
    rank_vacancies()
