from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Створити завдання")],
        [KeyboardButton(text="📥 Звіти на перевірці")],
        [KeyboardButton(text="🥇 Топ-10")],
        [
            KeyboardButton(text="👥 Учасники"),
            KeyboardButton(text="🥇 Рейтинг"),
        ],
    ],
    resize_keyboard=True,
)


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


def confirm_task_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Так, створити і розіслати",
                    callback_data="task_create_confirm",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Редагувати",
                    callback_data="task_create_edit",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="task_create_cancel",
                )
            ],
        ]
    )