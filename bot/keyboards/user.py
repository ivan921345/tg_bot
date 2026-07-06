from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

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


def confirm_report_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Так, я пiдтверджую звiт",
                    callback_data="report_confirm",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Редагувати",
                    callback_data="report_edit",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="report_cancel",
                )
            ],
        ]
    )