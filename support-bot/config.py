import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Не задана переменная {name}. Скопируйте .env.example в .env и заполните её."
        )
    return value


BOT_TOKEN = _require("BOT_TOKEN")
