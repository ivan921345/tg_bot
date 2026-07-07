from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.admin import admin_menu, confirm_task_keyboard, report_check_keyboard
from services.users import get_admin_ids, get_all_user_ids, get_all_users,update_user_crosses_count
from services.tasks import add_task
from services.reports import get_pending_reports, update_report_status,get_report_by_id

router = Router()


class CreateTask(StatesGroup):
    waiting_for_norm = State()
    waiting_for_code_word = State()
    waiting_for_confirm = State()


def is_admin(user_id: int) -> bool:
    return int(user_id) in get_admin_ids()


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
async def create_task_handler(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await state.set_state(CreateTask.waiting_for_norm)

    await message.answer(
        "📝 Створення завдання\n\n"
        "Введіть норму хрестиків:\n\n"
        "Наприклад: 300"
    )


@router.message(CreateTask.waiting_for_norm)
async def get_norm(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return

    if not message.text or not message.text.isdigit():
        await message.answer("❗ Введіть число, наприклад 300")
        return

    norm = int(message.text)

    if norm <= 0:
        await message.answer("❗ Норма має бути більше 0.")
        return

    await state.update_data(norm=norm)
    await state.set_state(CreateTask.waiting_for_code_word)

    await message.answer(
        "✅ Норму збережено.\n\n"
        "Тепер введіть кодове слово:"
    )


@router.message(CreateTask.waiting_for_code_word)
async def get_code_word(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return

    if not message.text:
        await message.answer("❗ Введіть кодове слово текстом.")
        return

    code_word = message.text.strip()

    if len(code_word) < 2:
        await message.answer("❗ Кодове слово занадто коротке.")
        return

    await state.update_data(code_word=code_word)

    data = await state.get_data()

    norm = data["norm"]
    code_word = data["code_word"]

    await state.set_state(CreateTask.waiting_for_confirm)

    await message.answer(
        "📋 Перевірте завдання:\n\n"
        f"🧵 Норма: {norm} хрестиків\n"
        f"🔑 Кодове слово: {code_word}\n\n"
        "Створити це завдання і розіслати всім учасникам?",
        reply_markup=confirm_task_keyboard(),
    )


@router.callback_query(F.data == "task_create_confirm")
async def task_create_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    data = await state.get_data()

    norm = data.get("norm")
    code_word = data.get("code_word")

    if not norm or not code_word:
        await callback.answer("Дані завдання не знайдено", show_alert=True)
        await state.clear()
        return

    user_ids = get_all_user_ids()
    add_task(code_word, norm)

    if len(user_ids) == 0:
        await callback.message.edit_text(
            "⚠️ Завдання створено, але немає учасників для розсилки.\n\n"
            f"🧵 Норма: {norm} хрестиків\n"
            f"🔑 Кодове слово: {code_word}"
        )
        await state.clear()
        return

    success = 0
    failed = 0

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=(
                    "🧵 Нове завдання!\n\n"
                    f"✅ Норма: {norm} хрестиків\n"
                    f"🔑 Кодове слово: {code_word}\n\n"
                    "Після виконання завдання надішліть звіт."
                ),
            )
            success += 1
        except Exception:
            failed += 1

    await callback.message.edit_text(
        "✅ Завдання створено і розіслано!\n\n"
        f"🧵 Норма: {norm} хрестиків\n"
        f"🔑 Кодове слово: {code_word}\n\n"
        f"👥 Успішно надіслано: {success}\n"
        f"⚠️ Не вдалося надіслати: {failed}"
    )

    await state.clear()
    await callback.answer("Завдання розіслано")


@router.callback_query(F.data == "task_create_edit")
async def task_create_edit_handler(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    await state.set_state(CreateTask.waiting_for_norm)

    await callback.message.edit_text(
        "✏️ Редагування завдання\n\n"
        "Введіть нову норму хрестиків:\n\n"
        "Наприклад: 300"
    )

    await callback.answer("Редагування")


@router.callback_query(F.data == "task_create_cancel")
async def task_create_cancel_handler(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    await state.clear()

    await callback.message.edit_text("❌ Створення завдання скасовано.")
    await callback.answer("Скасовано")


@router.message(F.text == "📥 Звіти на перевірці")
async def reports_handler(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    reports = get_pending_reports()

    if not reports:
        await message.answer("📭 Немає звітів на перевірці.")
        return

    await message.answer(
        f"📥 Неперевірених звітів: {len(reports)}"
    )

    for report in reports:
        report_id = report["id"]

        user = report["users"]
        formatted_date = datetime.fromisoformat(report["created_at"]).strftime("%d.%m.%Y %H:%M")

        username = user.get("username")
        full_name = user.get("full_name")

        username = f"@{username}" if username else "—"

        media = [
            InputMediaPhoto(
                media=report["first_photo"],
                caption=f"📸 Звіт №{report_id}\n\nФото ДО та ПІСЛЯ"
            ),
            InputMediaPhoto(
                media=report["second_photo"],
            ),
        ]

        await bot.send_media_group(
            chat_id=message.chat.id,
            media=media,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=(
                f"📋 <b>Звіт №{report_id}</b>\n\n"
                f"👤 {full_name}\n"
                f"🔗 {username}\n"
                f"📅 {formatted_date}\n\n"
                f"Статус: ⏳ Очікує перевірки"
            ),
            parse_mode="HTML",
            reply_markup=report_check_keyboard(report_id),
        )


@router.callback_query(F.data.startswith("approve_report:"))
async def approve_report_handler(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    report_id = int(callback.data.split(":")[1])

    update_report_status(report_id, "APPROVED")
    report_data = get_report_by_id(report_id)

    new_crosses_count=report_data["tasks"]["norm"]+report_data["users"]["crosses_count"]
    
    user_id = report_data["users"]["id"]
    user_tg_id = report_data["users"]["tg_id"]

    
    update_user_crosses_count(user_id, new_crosses_count)
    await callback.message.edit_text(
        f"✅ Звіт №{report_id} підтверджено."
    )
    
    media = [
        InputMediaPhoto(
            media=report_data["first_photo"],
            caption=f"✅ Ваш звіт №{report_id} підтверджено."
        ),
        InputMediaPhoto(
            media=report_data["second_photo"],
        ),
    ]   

    await bot.send_media_group(
        chat_id=user_tg_id,
        media=media,
    )
    await callback.answer("Звіт підтверджено")


@router.callback_query(F.data.startswith("reject_report:"))
async def reject_report_handler(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Немає доступу", show_alert=True)
        return

    report_id = int(callback.data.split(":")[1])

    update_report_status(report_id, "REJECTED")

    await callback.message.edit_text(
        f"❌ Звіт №{report_id} відхилено."
    )

    await callback.answer("Звіт відхилено")


@router.message(F.text == "👥 Учасники")
async def users_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = get_all_users()

    if not users:
        await message.answer("👥 Учасники\n\nПоки що учасників немає.")
        return

    response = "👥 Список учасників:\n\n"

    for index, user in enumerate(users, start=1):
        tg_id = user["tg_id"]
        username = user.get("username")
        full_name = user.get("full_name")
        crosses_count = user.get("crosses_count", 0)

        if username:
            name = f"@{username}"
        elif full_name:
            name = full_name
        else:
            name = f"Користувач {tg_id}"

        response += (
            f"{index}. {name}\n"
            f"   🆔 ID: {tg_id}\n"
            f"   👤 Імʼя: {full_name or 'не вказано'}\n"
            f"   🧵 Хрестиків: {crosses_count}\n\n"
        )

    await message.answer(response)


@router.message(F.text == "🥇 Рейтинг")
async def rating_handler(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🥇 Загальний рейтинг\n\n"
        "Поки що рейтинг порожній."
    )
