import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import menu


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # TG_API_BASE — адрес прокси до Bot API: из РФ api.telegram.org заблокирован с 30.09.2026.
    session = AiohttpSession(api=TelegramAPIServer.from_base(os.getenv("TG_API_BASE") or "https://api.telegram.org"))
    session._connector_init["keepalive_timeout"] = 5  # простаивающие соединения до Cloudflare рвутся по дороге
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp = Dispatcher()
    dp.include_router(menu.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=int(os.getenv("TG_POLL_TIMEOUT") or 7))


if __name__ == "__main__":
    asyncio.run(main())
