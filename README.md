# Job Scraper Bot

Автоматизированный парсер вакансий с ранжированием и отправкой лучших результатов в Telegram-бот.

## Возможности

- Авторизация на сайте
- Сбор ссылок на вакансии
- Парсинг информации о вакансиях
- Сохранение данных в CSV
- Ранжирование вакансий
- Отправка топовых результатов в Telegram

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/EugenePy3/hh_parser.git
   cd hh_parser

2. Создайте и активируйте виртуальное окружение:
python3 -m venv venv
source venv/bin/activate

3. Установите зависимости:
pip install -r requirements.txt

4. Создайте файл .env в директории scraper/ со своими настройками:
LOGIN=your_login
PASSWORD=your_password
TELEGRAM_TOKEN=your_token
CHAT_ID=your_chat_id

5. Запуск
python main.py

## 📁 Структура проекта
```markdown
├── main.py                 — точка входа
├── auth/
│   └── login.py            — авторизация
├── bot/
│   └── bot.py              — Telegram-бот
├── scraper/
│   ├── browser.py          — запуск драйвера
│   ├── config.py           — настройки
│   ├── parser.py           — парсинг ссылок
│   ├── vacancy_scraper.py  — парсинг вакансий
│   └── .env                — переменные окружения
├── utils/
│   ├── file_operations.py  — сохранение данных
│   ├── ranking.py          — ранжирование
│   └── logger.py           — логирование
├── tests/
│   └── ...                 — тесты проекта
├── vacancies_1.csv         — сохранённые вакансии
├── requirements1.txt       — зависимости
└── README.md               — документация
```

Используется:
    selenium
    pandas
    python-dotenv
    aiogram

## . gitignore
```
venv/
__pycache__/
*.pyc
.env
.vscode/
.idea/
*.log
vacancies_*.csv
ranked_vacancies_*.csv
```
 Автор:
    Сделано с упорством и мечтой стать разработчиком 🙌
    Eugene 😻

hh-vacancy-bot