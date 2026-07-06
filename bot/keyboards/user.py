from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from services.users import add_user, get_user_by_tg_id
router = Router()


user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Завдання")],
        [KeyboardButton(text="📸 Надіслати звіт")],
        [
            KeyboardButton(text="🏆 Мій результат"),
            KeyboardButton(text="🥇 Топ-10"),
        ],
        [KeyboardButton(text="📖 Правила гри")],
    ],
    resize_keyboard=True,
)


@router.message(F.text == "/start")
async def start_handler(message: Message):

    print(message.from_user.username, message.from_user.full_name)
    if(get_user_by_tg_id(message.from_user.id) == -1):
        add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    
    await message.answer(
        "🎮 Вітаємо у грі!\n\nОберіть потрібну дію:",
        reply_markup=user_menu,
    )


@router.message(F.text == "📋 Завдання")
async def today_task_handler(message: Message):
    await message.answer(
        "📋 Завдання на сьогодні\n\n"
        "🔹 Норма: 500 хрестиків\n"
        "🔹 Кодове слово: Маяк\n\n"
        "Зробіть фото ДО, вишийте норму та надішліть фото ПІСЛЯ."
    )


@router.message(F.text == "📸 Надіслати звіт")
async def send_report_handler(message: Message):
    await message.answer(
        "📸 Надсилання звіту\n\n"
        "Поки що це демо.\n\n"
        "У повній версії бот попросить:\n"
        "1. Фото ДО\n"
        "2. Фото ПІСЛЯ\n"
        "3. Кількість хрестиків"
    )


@router.message(F.text == "🏆 Мій результат")
async def my_result_handler(message: Message):
    await message.answer(
        "🏆 Ваш результат\n\n"
        "Всього вишито: 0 хрестиків\n"
        "Місце у рейтингу: поки немає"
    )


@router.message(F.text == "🥇 Топ-10")
async def top_10_handler(message: Message):
    await message.answer(
        "🥇 Топ-10 учасників\n\n"
        "Поки що рейтинг порожній."
    )


@router.message(F.text == "📖 Правила гри")
async def rules_handler(message: Message):
    await message.answer(
        "📖 Правила гри\n\n"
        "• Щодня бот надсилає завдання.\n"
        "• Учасник робить фото ДО з кодовим словом.\n"
        "• Потім вишиває норму.\n"
        "• Робить фото ПІСЛЯ.\n"
        "• Адміністратор перевіряє звіт.\n"
        "• Після підтвердження хрестики додаються до рейтингу."
    )