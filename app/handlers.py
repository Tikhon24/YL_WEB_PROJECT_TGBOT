from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


class AddAdForm(StatesGroup):
    title = State()
    description = State()
    image = State()
    price = State()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("*старт*", reply_markup=kb.start)


@router.message(Command("help"))
async def get_help(message: Message) -> None:
    await message.answer("*помощь*")


@router.message(Command("add_ad"))
async def add_ad_first(message: Message, state: FSMContext):
    await state.set_state(AddAdForm.title)
    await message.answer("Введите название обявления:")


@router.message(AddAdForm.title)
async def add_ad_second(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddAdForm.description)
    await message.answer("Введите описание товара:")


@router.message(AddAdForm.description)
async def add_ad_third(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddAdForm.image)
    await message.answer("Отправте картинку:", reply_markup=kb.without_image)


@router.message(AddAdForm.image)
async def add_ad_fourth1(message: Message, state: FSMContext):
    await state.update_data(name=message.photo)
    await state.set_state(AddAdForm.price)
    await message.answer("Введите цену товара(₽):")


@router.callback_query(lambda c: c.data == "no_image")
async def add_ad_fourth2(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Подтверждаем нажатие кнопки
    await state.update_data(image="")  # Устанавливаем значение для изображения
    await state.set_state(AddAdForm.price)


@router.message(AddAdForm.price)
async def add_ad_fifth(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)

    except ValueError:
        await message.answer("Пожалуйста, введите корректную цену (число). Попробуйте снова:")

