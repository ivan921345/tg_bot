from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.user import confirm_report_keyboard, user_menu
from services.reports import add_report, get_pending_reports_count
from services.tasks import get_last_task
from services.users import add_user, get_admin_ids, get_user_by_tg_id

router = Router()


class ReportState(StatesGroup):
    waiting_first_photo = State()
    waiting_second_photo = State()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    user = message.from_user

    if get_user_by_tg_id(user.id) == -1:
        add_user(user.id, user.username, user.full_name)

    await message.answer(
        "🎮 Вітаємо у грі!\n\nОберіть потрібну дію:",
        reply_markup=user_menu,
    )


@router.message(F.text == "📋 Завдання")
async def today_task_handler(message: Message):
    task = get_last_task()

    if not task:
        await message.answer("📋 Завдання на сьогодні ще не створено.")
        return

    await message.answer(
        "📋 Завдання на сьогодні\n\n"
        f"🔹 Норма: {task['norm']} хрестиків\n"
        f"🔹 Кодове слово: {task['code_word']}\n\n"
        "Зробіть фото ДО, вишийте норму та надішліть фото ПІСЛЯ."
    )


@router.message(F.text == "📸 Надіслати звіт")
async def send_report_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ReportState.waiting_first_photo)

    await message.answer("📸 Надішліть перше фото ДО з кодовим словом.")


@router.message(ReportState.waiting_first_photo, F.photo)
async def get_first_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]

    await state.update_data(
        tg_id=message.from_user.id,
        first_photo=photo.file_id,
    )

    await state.set_state(ReportState.waiting_second_photo)

    await message.answer(
        "📸 Тепер надішліть друге фото ПІСЛЯ з результатом і кодовим словом."
    )


@router.message(ReportState.waiting_second_photo, F.photo)
async def get_second_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]

    await state.update_data(second_photo=photo.file_id)

    await message.answer(
        "📋 Підтвердження звіту\n\n"
        "Перевірте, чи все правильно.",
        reply_markup=confirm_report_keyboard(),
    )


@router.callback_query(F.data == "report_confirm")
async def report_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()

    tg_id = data.get("tg_id")
    first_photo = data.get("first_photo")
    second_photo = data.get("second_photo")

    if not tg_id or not first_photo or not second_photo:
        await callback.answer("Дані звіту не знайдено", show_alert=True)
        await state.clear()
        return

    add_report(tg_id, first_photo, second_photo)

    pending_reports_count = get_pending_reports_count()
    admin_ids = get_admin_ids()

    for admin_id in admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    "📥 Надіслано новий звіт!\n\n"
                    f"📋 Неперевірених звітів: {pending_reports_count}"
                ),
            )
        except Exception:
            pass

    await callback.message.edit_text("✅ Звіт успішно надіслано на перевірку.")
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "report_edit")
async def report_edit_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ReportState.waiting_first_photo)

    await callback.message.edit_text(
        "✏️ Редагування звіту\n\n"
        "Надішліть перше фото ДО з кодовим словом."
    )

    await callback.answer()


@router.callback_query(F.data == "report_cancel")
async def report_cancel_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text("❌ Надсилання звіту скасовано.")
    await callback.answer()


@router.message(F.text == "🏆 Мій результат")
async def my_result_handler(message: Message):
    await message.answer(
        "🏆 Ваш результат\n\n"
        "Всього вишито: 0 хрестиків\n"
        "Місце у рейтингу: поки немає"
    )


@router.message(F.text == "🥇 Топ-10")
async def top_10_handler(message: Message):
    await message.answer("🥇 Топ-10 учасників\n\nПоки що рейтинг порожній.")


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