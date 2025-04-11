import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

#  настройки авторизации (если прописаны в .env)
#  Загружаем логин и пароль из переменной окружения
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# Пути и основные настройки
CHROME_DRIVER_PATH = '/usr/bin/chromedriver'  # путь к chrome драйверу
BASE_URL = 'https://novosibirsk.hh.ru/'  # город для выбора
SEARCH_QUERY = 'Python разработчик'
MAX_PAGES = 2  # количество страниц для парсинга

# Настройки ранжирования:
# Зарплата:
SALARY_WEIGHT = 0.3  # зарплата даёт 0.3 балла за каждую 1000₽
SALARY_MAX_SCORE = 30  # максимально 30 баллов за зарплату

#  опыт работы:
EXPERIENCE_SCORES = {
    'менее 1': 40,
    'без опыта': 35,
    '1': 30,
    '2': 20,
    '3': 0,
    '4': 0,
    '5': -20,
    'более 5': -20
}

#  формат работы:
WORK_FORMAT_KEYWORDS = ['удал', 'гибкий', 'частич', 'проектн', 'совмещ']
WORK_FORMAT_SCORE = 20

# Рабочий стек начинающего (по количеству совпадений)
STACK = [
    'python', 'selenium', 'flask', 'django',
    'git', 'html', 'css', 'json', 'sqlite',
    'requests', 'bs4', 'asyncio', 'docker',
    'oop', 'etree', 'logging'
]
STACK_SCORE = {
    1: 5,
    2: 8,
    3: 10,
}

#  ключевые слова в описании:
KEYWORDS = ['python', 'selenium', 'автоматизация']
KEYWORD_SCORE = 10

#  ключевые слова для Джунов:
JUNIOR_KEYWORDS = ['готовы обуч', 'менторство', 'развитие', 'готовы рассмотреть без опыта']
JUNIOR_SCORE = 30

#  Заголовок вакансии - Если в заголовке вакансии есть Junior/Intern - большой бонус
JUNIOR_TITLES = ['junior', 'джун', 'стажер', 'начинающий', 'младший']
JUNIOR_TITLE_SCORE = 30

INTERN_TITLES = ['intern', 'стажировка']
INTERN_TITLE_SCORE = 40

# Если в заголовке вакансии есть 'senior', 'lead', 'team lead' штраф 40 баллов.
SENIOR_TITLES = ['senior', 'lead', 'team lead']
SENIOR_PENALTY = 40

# Если в заголовке вакансии есть 'pre-middle', 'pre middle', 'fullstack', 'фулстек' штраф 20 баллов.
PRE_MIDDLE_TITLES = ['pre-middle', 'pre middle']
FULLSTACK_TITLES = ['fullstack', 'фулстек']
# обьединим
NOT_JUNIOR_TITLES = PRE_MIDDLE_TITLES + FULLSTACK_TITLES
NOT_JUNIOR_PENALTY = 20  # штраф 20 баллов

# Подозрительные описания для Junior — даём штраф 25 баллов.
NOT_JUNIOR_KEYWORDS = [
    '1–3 года', '1-3 года', 'от 1 года опыта', 'без ментора',
    'самостоятельная работа', 'быстро влиться в проект',
    'опыт в проде', 'production', 'бенч', 'bench', 'в очередь'
]
NOT_JUNIOR_DESCRIPTION_PENALTY = 25

# Недавно опубликованные вакансии
RECENT_VACANCY_BONUS_DAYS = 3
RECENT_VACANCY_BONUS_SCORE = 15

#  Настройка для Телеграмм Бота

# Получаем токен and CHAT_ID из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RANKED_CSV = "ranked_vacancies.csv"  # Файл с вакансиями
TOP_N = 10  # Количество вакансий для отправки
