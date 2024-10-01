import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from avito_api import get_avito_items, get_call_stats
from excel_report import create_xlsx_report

API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Временное хранилище токенов пользователей 
user_tokens = {}

# Логгирование
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать! Отправьте мне ваш токен Avito, чтобы получить статистику звонков.")

@dp.message(Command("add_token"))
async def add_token(message: types.Message):
    token = message.text.split(maxsplit=1)[1]
    user_id = message.from_user.id
    if user_id in user_tokens:
        user_tokens[user_id].append(token)
    else:
        user_tokens[user_id] = [token]
    await message.answer("Токен сохранен. Вы можете добавить еще один токен или продолжить парсинг.")

@dp.message(Command("parse"))
async def parse_avito(message: types.Message):
    user_id = message.from_user.id
    tokens = user_tokens.get(user_id)

    if not tokens:
        await message.answer("Пожалуйста, сначала отправьте токен через команду /add_token.")
        return

    await message.answer("Начинаю парсинг ваших объявлений. Это может занять некоторое время...")

    data = {}
    for token in tokens:
        items = await get_avito_items(token)
        for item in items.get("items", []):
            stats = await get_call_stats(token, item["user_id"])
            data[item["user_id"]] = stats

    report = create_xlsx_report(data)
    report.save("avito_report.xlsx")

    with open("avito_report.xlsx", "rb") as file:
        await message.answer_document(file, caption="Вот ваша статистика звонков.")

if __name__ == "__main__":
    dp.run_polling(bot)
