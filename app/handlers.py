from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.other_funcs as of
import app.requests_funcs as rf

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
    await message.answer("*помощь*", reply_markup=kb.without_image)


@router.message(Command("add_ad"))
async def add_ad_first(message: Message, state: FSMContext):
    await state.set_state(AddAdForm.title)
    await message.answer("Введите название обявления:")


@router.message(AddAdForm.title)
async def add_ad_second(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddAdForm.description)
    await message.answer("Введите описание товара:")


@router.message(AddAdForm.description)
async def add_ad_third(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddAdForm.image)
    await message.answer("Отправте картинку:", reply_markup=kb.without_image)


@router.message(AddAdForm.image)
async def add_ad_fourth1(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await state.set_state(AddAdForm.price)
    await message.answer("Введите цену товара(₽):")


@router.callback_query(lambda c: c.data == "no_image")
async def process_no_image(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(image="")
    await state.set_state(AddAdForm.price)
    await callback_query.message.answer("Введите цену товара(₽):")

class AdData(StatesGroup):
    data = State()


@router.message(AddAdForm.price)
async def add_ad_fifth(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        data = await state.get_data()
        data["user_tag"] = message.from_user.username
        data["ads_id"] = rf.get("/get_ad_id")['ad_id']
        ad_message, image_id = await of.create_ad_message(data)
        await message.answer_photo(photo=image_id, caption=ad_message, parse_mode='Markdown', reply_markup=kb.ready_ad)
        await state.set_state(AdData.data)
        await state.update_data(data=data)
    except ValueError:
        await message.answer("Пожалуйста, введите корректную цену (число). Попробуйте снова:")


@router.callback_query(lambda c: c.data == "publish")
async def publish(callback: CallbackQuery):
    data = await state.get_data()
    data = data.get("data")
    print(data)