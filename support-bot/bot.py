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
    # Через прокси getUpdates иногда виснет: ждём не session.timeout + polling, а polling + 8 с.
    from aiogram.methods import GetUpdates
    _make_request = session.make_request

    async def _make_request_capped(bot, method, timeout=None):
        if isinstance(method, GetUpdates):
            timeout = (method.timeout or 0) + 8
        return await _make_request(bot, method, timeout=timeout)

    session.make_request = _make_request_capped
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp = Dispatcher()
    dp.include_router(menu.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=int(os.getenv("TG_POLL_TIMEOUT") or 7))


if __name__ == "__main__":
    asyncio.run(main())
