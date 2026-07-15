from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()

SITE_URL = "https://botansfree.ru"
EXPERT_URL = "https://t.me/botans_free"

WELCOME = (
    "Я бот <b>Botans free</b> — разработка Telegram-ботов под ключ.\n\n"
    "Выберите, что нужно:"
)

BACK_KB = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]]
)

# ключ -> (вопрос, ответ)
FAQ = {
    "1": (
        "Сколько по времени занимает создание ботов?",
        "Зависит от сложности продукта и загруженности заказов. "
        "В среднем от 6 часов до 1 недели.",
    ),
    "2": (
        "Почему так дорого?",
        "Цена полностью оправдывает свой продукт: на других площадках с похожими "
        "услугами вы найдёте цену только больше. У нас один из лучших ценников, "
        "который оправдывает ожидания покупателей.",
    ),
    "3": (
        "Можно ли внести правки спустя пару дней?",
        "Да, простые правки бесплатны в течение недели после завершения работы "
        "над ботом. После — правки стоят от 500 ₽. Можно договориться о "
        "безлимитных правках на определённый период, если бот требует "
        "постоянных обновлений.",
    ),
}


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Частые вопросы", callback_data="faq")],
            [InlineKeyboardButton(text="Каталог ботов", callback_data="catalog")],
            [InlineKeyboardButton(text="Сайт", url=SITE_URL)],
            [InlineKeyboardButton(text="Заказать бота", url=EXPERT_URL)],
        ]
    )


def faq_list_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=question, callback_data=f"faq:{key}")]
        for key, (question, _answer) in FAQ.items()
    ]
    rows.append([InlineKeyboardButton(text="Не нашли ответ? Напишите эксперту.", url=EXPERT_URL)])
    rows.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_menu_kb())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer("Нажмите /start, чтобы открыть меню.")


@router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Каталог ботов\n\nСкоро будет добавлен.",
        reply_markup=BACK_KB,
    )
    await callback.answer()


@router.callback_query(F.data == "faq")
async def show_faq_list(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Частые вопросы", reply_markup=faq_list_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("faq:"))
async def show_faq_answer(callback: CallbackQuery) -> None:
    item = FAQ.get(callback.data.split(":", 1)[1])
    if item is None:
        await callback.answer()
        return
    question, answer = item
    await callback.message.edit_text(
        f"{question}\n\n{answer}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="faq")]]
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(WELCOME, reply_markup=main_menu_kb())
    await callback.answer()
