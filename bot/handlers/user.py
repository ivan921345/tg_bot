from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from services.users import add_user, get_user_by_tg_id
from keyboards.user import user_menu,confirm_report_keyboard
from services.tasks import get_last_task
from aiogram.fsm.context import FSMContext

router = Router()

class ReportState(StatesGroup):
    waiting_first_photo = State()
    waiting_second_photo = State()

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
    task = get_last_task()
    await message.answer(
        "📋 Завдання на сьогодні\n\n"
        f"🔹 Норма: {task["norm"]} хрестиків\n"
        f"🔹 Кодове слово: {task["code_word"]}\n\n"
        "Зробіть фото ДО, вишийте норму та надішліть фото ПІСЛЯ."
    )


@router.message(F.text == "📸 Надіслати звіт")
async def send_report_handler(message: Message,state: FSMContext):
    await state.clear()
    await state.set_state(ReportState.waiting_first_photo)
    await message.answer(
        "📸 Надішліть перше фото ДО з кодовим словом"
    )
@router.message(ReportState.waiting_first_photo, F.photo)
async def get_first_photo(message: Message, state: FSMContext):
    photo = message.photo[-1] 
    
    await state.update_data(
        first_photo=photo.file_id
    )

    await state.set_state(ReportState.waiting_second_photo)

    await message.answer("Надішліть друге фото ПIСЛЯ з результатом разом з кодовим словом.")
@router.message(ReportState.waiting_second_photo, F.photo)
async def get_first_photo(message: Message, state: FSMContext):
    photo = message.photo[-1] 
    
    await state.update_data(
        second_photo=photo.file_id
    )


    
    await message.answer(
        "📋 Пiдвердження звiту\n",
        reply_markup=confirm_report_keyboard()
    )


@router.callback_query(F.data == "report_confirm")
async def report_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    print("1")

@router.callback_query(F.data == "report_edit")
async def report_edit_handler(callback: CallbackQuery, state: FSMContext):
   print("2")


@router.callback_query(F.data == "report_cancel")
async def report_cancel_handler(callback: CallbackQuery, state: FSMContext):
   print("3")



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