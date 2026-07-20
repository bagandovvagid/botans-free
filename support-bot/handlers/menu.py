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


# порядок = порядок кнопок в каталоге; цена — базовая, «от»
CATALOG = {
    "support": {
        "name": "Бот поддержки",
        "price": "от 2 500 ₽",
        "text": (
            "<b>Бот поддержки</b> — первая линия, которая отвечает мгновенно "
            "и ничего не теряет: FAQ, приём заявок, передача менеджеру.\n\n"
            "<b>Почему такая цена:</b> это самый отработанный тип бота — "
            "логика типовая, поэтому и ценник один из самых доступных. "
            "Дороже выйдет, если нужны несколько менеджеров по темам, "
            "статистика обращений и оценка ответов клиентами."
        ),
    },
    "moderator": {
        "name": "Модератор чата",
        "price": "от 2 500 ₽",
        "text": (
            "<b>Модератор чата</b> — держит порядок круглосуточно: спам "
            "исчезает, нарушители получают ограничения, новичков встречают "
            "правила.\n\n"
            "<b>Почему такая цена:</b> класс ботов проверенный, много готовых "
            "наработок — поэтому недорого. Дороже, если нужны свои правила "
            "под чат, капча для новичков, белые списки и отчёты админам."
        ),
    },
    "broadcast": {
        "name": "Бот рассылок",
        "price": "от 3 500 ₽",
        "text": (
            "<b>Бот рассылок</b> — доносит нужное сообщение до нужных людей "
            "вовремя и без ручной работы: рассылки, автоворонки, статистика.\n\n"
            "<b>Почему такая цена:</b> база несложная, но есть скрытая работа — "
            "Telegram ограничивает скорость отправки, и рассылать надо "
            "аккуратно, чтобы бот не поймал блокировку. Дороже — за "
            "автоворонки, сегментацию аудитории и подробную статистику."
        ),
    },
    "archiver": {
        "name": "Бот-архиватор",
        "price": "от 4 500 ₽",
        "text": (
            "<b>Бот-архиватор</b> — ничего не пропадает: сохраняет переписку "
            "и медиа, а когда сообщение удалили или изменили — оригинал "
            "остаётся у вас.\n\n"
            "<b>Почему такая цена:</b> задача нестандартная, готовых шаблонов "
            "мало. Telegram не сообщает об удалении — нужно заранее сохранять "
            "весь поток и хранить медиа, а бот должен работать без перерывов. "
            "Дороже — за архив медиа, несколько чатов и поиск по словам."
        ),
    },
    "booking": {
        "name": "Бот записи",
        "price": "от 4 500 ₽",
        "text": (
            "<b>Бот записи</b> — клиенты записываются сами, без звонков "
            "и ожиданий: календарь свободных окон, напоминания, переносы.\n\n"
            "<b>Почему такая цена:</b> календарь — капризная часть: "
            "пересечения, переносы, отмены, несколько мастеров. Просроченное "
            "напоминание = потерянный клиент, поэтому всё тщательно "
            "тестируется. Дороже — за несколько мастеров и услуг, предоплату "
            "и синхронизацию с вашим календарём."
        ),
    },
    "paywall": {
        "name": "Продажа доступа к каналу",
        "price": "от 5 000 ₽",
        "text": (
            "<b>Продажа доступа к каналу</b> — продаёт подписку на закрытый "
            "канал и сам следит, чтобы доступ был только у оплативших.\n\n"
            "<b>Почему такая цена:</b> это работа с деньгами — оплаты "
            "и продления должны сходиться копейка в копейку, а доступ "
            "выдаваться и отзываться вовремя. Цена ошибки высокая: сбой "
            "клиент заметит сразу. Дороже — за несколько тарифов, пробный "
            "период, автопродление и промокоды."
        ),
    },
    "ai": {
        "name": "ИИ-бот",
        "price": "от 5 500 ₽",
        "text": (
            "<b>ИИ-бот</b> — консультант, который не спит: отвечает клиентам "
            "мгновенно на базе ChatGPT и говорит на языке вашего бизнеса.\n\n"
            "<b>Почему такая цена:</b> подключить нейросеть просто, а вот "
            "заставить её отвечать строго по вашим материалам и без "
            "отсебятины — это и есть работа. Плюс настройка тона и передачи "
            "сложных вопросов менеджеру. Дороже — за большую базу знаний, "
            "память о клиентах и понимание голосовых."
        ),
    },
    "community": {
        "name": "Геймификация сообщества",
        "price": "от 5 500 ₽",
        "text": (
            "<b>Геймификация сообщества</b> — превращает чат в игру: участники "
            "зарабатывают баллы, растут в уровнях и соревнуются — активность "
            "растёт сама.\n\n"
            "<b>Почему такая цена:</b> нужен постоянный фоновый учёт активности "
            "каждого участника, а баланс игры настраивается вручную, чтобы "
            "было интересно и нельзя было накрутить. Дороже — за уровни "
            "и звания, магазин наград, сезоны и защиту от накрутки."
        ),
    },
    "shop": {
        "name": "Бот-магазин",
        "price": "от 7 500 ₽",
        "text": (
            "<b>Бот-магазин</b> — полноценный магазин внутри Telegram: "
            "от витрины до оплаты, без сайта и приложения.\n\n"
            "<b>Почему такая цена:</b> это самая большая связка функций — "
            "каталог, корзина, заказы, статусы, промокоды, остатки. Плюс "
            "приём оплаты: тестовые платежи и обработка ошибок, ведь это "
            "чужие деньги. Дороже — за онлайн-оплату, учёт остатков "
            "и загрузку товаров из таблицы."
        ),
    },
    "monitoring": {
        "name": "Мониторинг и сбор данных",
        "price": "от 7 500 ₽",
        "text": (
            "<b>Мониторинг и сбор данных</b> — следит за нужными площадками "
            "вместо вас и присылает только то, что подходит под ваши "
            "критерии.\n\n"
            "<b>Почему такая цена:</b> площадки вроде Авито защищаются от "
            "автоматического сбора — обход этих защит и есть основная "
            "сложность. Сайты меняют структуру, сбор ломается, поэтому "
            "в цену заложена стабилизация. Дороже — за несколько площадок, "
            "историю цен и отчёты таблицей."
        ),
    },
    "docs": {
        "name": "ИИ-обработка документов",
        "price": "от 10 000 ₽",
        "text": (
            "<b>ИИ-обработка документов</b> — сфотографируйте документ, "
            "и бот сам распознает данные, заполнит шаблон и подготовит "
            "готовую бумагу.\n\n"
            "<b>Почему такая цена:</b> задача двойная — распознать данные "
            "с фото (качество снимков у всех разное) и без ошибок разложить "
            "по шаблону. Цена ошибки высокая: документы должны быть точными, "
            "нужно тестировать на реальных примерах. Дороже — за несколько "
            "типов документов и сложные шаблоны с условиями."
        ),
    },
    "miniapp": {
        "name": "Mini App — приложение в Telegram",
        "price": "от 15 000 ₽",
        "text": (
            "<b>Mini App</b> — полноценное приложение прямо в Telegram: "
            "кнопки, карточки, каталоги, без установки и регистрации.\n\n"
            "<b>Почему такая цена:</b> это фактически два проекта — визуальный "
            "интерфейс, как мини-сайт, плюс бот-логика за ним. Нужен дизайн "
            "экранов под телефон и компьютер. Самый «вау»-продукт, рынок "
            "оценивает его выше всего. Дороже — за онлайн-оплату, личный "
            "кабинет и дизайн под ваш фирменный стиль."
        ),
    },
}

CATALOG_INTRO = (
    "<b>Каталог ботов</b>\n\n"
    "Нажмите на любого бота — расскажу, что он умеет и почему стоит "
    "именно столько. Цена указана за базовую версию, «от» — итог зависит "
    "от ваших пожеланий."
)


def catalog_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{bot['name']} · {bot['price']}", callback_data=f"bot:{key}")]
        for key, bot in CATALOG.items()
    ]
    rows.append([InlineKeyboardButton(text="Заказать бота", url=EXPERT_URL)])
    rows.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def bot_info_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Заказать этого бота", url=EXPERT_URL)],
            [InlineKeyboardButton(text="Назад в каталог", callback_data="catalog")],
        ]
    )


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
    await callback.message.edit_text(CATALOG_INTRO, reply_markup=catalog_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("bot:"))
async def show_bot_info(callback: CallbackQuery) -> None:
    bot = CATALOG.get(callback.data.split(":", 1)[1])
    if bot is None:
        await callback.answer()
        return
    await callback.message.edit_text(bot["text"], reply_markup=bot_info_kb())
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
