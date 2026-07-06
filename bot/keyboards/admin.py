from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
import os
from dotenv import load_dotenv

load_dotenv()

router = Router()

ADMIN_IDS_ENV = os.getenv("ADMIN_IDS")
ADMIN_IDS = ADMIN_IDS_ENV.split(",") if ADMIN_IDS_ENV else []


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Створити завдання")],
        [KeyboardButton(text="📥 Звіти на перевірці")],
        [
            KeyboardButton(text="👥 Учасники"),
            KeyboardButton(text="🥇 Рейтинг"),
        ],
    ],
    resize_keyboard=True,
)


def is_admin(user_id: int) -> bool:
    return  str(user_id) in ADMIN_IDS


def report_check_keyboard(report_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Підтвердити",
                    callback_data=f"approve_report:{report_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data=f"reject_report:{report_id}",
                ),
            ]
        ]
    )


@router.message(F.text == "/admin")
async def admin_start_handler(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас немає доступу до адмін-панелі.")
        return

    await message.answer(
        "👑 Панель адміністратора\n\nОберіть потрібну дію:",
        reply_markup=admin_menu,
    )


@router.message(F.text == "📝 Створити завдання")
async def create_task_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📝 Створення завдання\n\n"
        "Поки що це демо.\n\n"
        "У повній версії тут адмін буде вводити:\n"
        "1. Норму хрестиків\n"
        "2. Кодове слово\n"
        "3. Бот розішле завдання всім учасникам"
    )


@router.message(F.text == "📥 Звіти на перевірці")
async def reports_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📥 Звіти на перевірці\n\n"
        "Поки що нових звітів немає."
    )


@router.message(F.text == "👥 Учасники")
async def users_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👥 Учасники\n\n"
        "Поки що список учасників порожній."
    )


@router.message(F.text == "🥇 Рейтинг")
async def rating_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🥇 Загальний рейтинг\n\n"
        "Поки що рейтинг порожній."
    )




@router.callback_query(F.data.startswith("approve_report:"))
async def approve_report_handler(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    report_id = callback.data.split(":")[1]

    await callback.message.edit_text(
        f"✅ Звіт №{report_id} підтверджено."
    )
    await callback.answer("Звіт підтверджено")


@router.callback_query(F.data.startswith("reject_report:"))
async def reject_report_handler(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    report_id = callback.data.split(":")[1]

    await callback.message.edit_text(
        f"❌ Звіт №{report_id} відхилено."
    )
    await callback.answer("Звіт відхилено")