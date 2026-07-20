"""
Приём заявок с сайта — фрагмент для встраивания в существующего бота.

Это не готовый бот: здесь только хендлеры, объекты dp/bot берутся из вашего проекта.

Два пути, по которым приходит заявка с сайта:
  1. Mini App — форма вызывает tg.sendData(), прилетает message.web_app_data.
     Важно: web_app_data приходит ТОЛЬКО если Mini App открыт кнопкой
     клавиатуры (KeyboardButton с web_app=...). Через меню-кнопку или
     inline-кнопку sendData не сработает — заявка не дойдёт.
  2. Обычный браузер — пользователь попадает в чат с ботом с готовым
     текстом заявки и отправляет его сам обычным сообщением.
"""

import json

from aiogram import F
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

SITE_URL = "https://botansfree.ru"

BOT_TITLES = {
    "archiver": "Бот-архиватор",
    "support": "Бот поддержки",
    "shop": "Бот-магазин",
    "booking": "Бот записи",
    "broadcast": "Бот рассылок",
    "ai": "ИИ-бот",
    "": "не определился",
}


@dp.message(F.web_app_data)
async def handle_lead(message: Message):
    data = json.loads(message.web_app_data.data)

    await message.answer("Заявка получена, свяжусь в течение дня")

    # Себе — та же заявка в читаемом виде
    await bot.send_message(
        ADMIN_ID,
        "Заявка с сайта\n"
        f"Имя: {data.get('name', '—')}\n"
        f"Ниша: {data.get('niche', '—')}\n"
        f"Бот: {BOT_TITLES.get(data.get('bot_type', ''), data.get('bot_type'))}\n"
        f"Комментарий: {data.get('comment') or '—'}\n"
        f"От: @{message.from_user.username or message.from_user.id}",
    )


@dp.message(F.text.startswith("ЗАЯВКА:"))
async def handle_lead_text(message: Message):
    """Тот же ответ для заявок из браузера — они приходят обычным текстом."""
    await message.answer("Заявка получена, свяжусь в течение дня")
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)


@dp.message(F.text == "/start")
async def start(message: Message):
    """Кнопка, из которой Mini App может слать sendData."""
    await message.answer(
        "Открыть форму заявки:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Оставить заявку", web_app=WebAppInfo(url=SITE_URL))]],
            resize_keyboard=True,
        ),
    )
