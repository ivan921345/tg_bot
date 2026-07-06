from aiogram.types import KeyboardButton,ReplyKeyboardMarkup



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

