import os
import asyncio
import logging

import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold, hlink
from aiogram.client.bot import DefaultBotProperties

from scraper.config import RANKED_CSV, TOP_N, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Файл с вакансиями Вынесено в конфиг
#  RANKED_CSV = "ranked_vacancies.csv"
# TOP_N = 10  # Количество вакансий для отправки


# Функция для загрузки вакансий
def load_vacancies():
    if not os.path.exists(RANKED_CSV):
        logging.error('Файл с вакансиями не найден!')
        return None

    try:
        df = pd.read_csv(RANKED_CSV).head(TOP_N)
        logging.info(f'Загружено {len(df)} вакансий.')
        #  df = df.sort_values(by="score", ascending=False).head(TOP_N)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f'Ошибка при загрузке вакансий: {e}')
        return None


# Функция для отправки вакансий
async def send_vacancies():
    vacancies = load_vacancies()
    if not vacancies:
        await bot.send_message(TELEGRAM_CHAT_ID, '❌ Вакансии не найдены.')
        return

    for vacancy in vacancies:
        try:
            vacancy_url = vacancy.get('url', '#') or '#'
            response_link = vacancy.get('response_link', '#') or '#'
            phone_number = vacancy.get('phone_number', 'не указан')
            email_contact = vacancy.get('email_contact', 'не указан')

            text = (f"💼 {hbold(vacancy['title'])}\n"
                    f"⭐ <b>Присвоенный балл:</b> {vacancy['score']}\n"
                    f"💰 <b>Зарплата:</b> {vacancy['salary']} руб.\n"
                    f"📅 <b>Опыт:</b> {vacancy['experience']}\n"
                    f"🏢 <b>Занятость:</b> {vacancy['common_employment']}\n"
                    f"⏳ <b>График:</b> {vacancy['works_schedule']}\n"
                    f"🕒 <b>Рабочие часы:</b> {vacancy['working_hours']}\n"
                    f"🧑‍💻 <b>Формат работы:</b> {vacancy['work_formats']}\n"
                    f"🗓 <b>Дата публикации:</b> {vacancy['date']}\n"
                    f"📞 <b>Позвонить:</b> {phone_number}\n"
                    f"✉️ <b>Написать на почту:</b> {email_contact}\n"
                    f"🔗 {hlink('Ссылка на вакансию', vacancy_url)}\n"
                    f"✉️ {hlink('Откликнуться на вакансию', response_link)}\n")

            # Обрезка длинного описания
            description = vacancy['description']
            if len(description) > 400:
                description = description[:400] + "...\n📝 <i>Описание сокращено</i>"
            text += f"\n📝 <b>Описание:</b> {description}"

            await bot.send_message(TELEGRAM_CHAT_ID, text=text)
            logging.info(f'Вакансия {vacancy["title"]} отправлена в Телеграмм')

            await asyncio.sleep(2)  # Небольшая задержка

        except Exception as e:
            logging.error(f'Ошибка при отправке вакансии: {e}')


# Основная асинхронная функция запуска
async def main():
    asyncio.create_task(send_vacancies())
    # dp.startup.register(send_vacancies)  # Автоматическая отправка при старте
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
