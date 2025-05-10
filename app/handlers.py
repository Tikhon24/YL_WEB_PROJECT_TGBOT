from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot

import app.other_funcs as of
import app.requests_funcs as rf

import app.keyboards as kb

router = Router()


class AddAdForm(StatesGroup):
    title = State()
    description = State()
    image = State()
    price = State()
    user_tag = State()
    ads_id = State()


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
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        await state.set_state(AddAdForm.price)
        await message.answer("Введите цену товара(₽):")
    else:
        await message.answer("Пожалуйста, отправьте фото.")


@router.callback_query(lambda c: c.data == "no_image")
async def process_no_image(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(image="")
    await state.set_state(AddAdForm.price)
    await callback_query.message.answer("Введите цену товара(₽):")


@router.message(AddAdForm.price)
async def add_ad_fifth(message: Message, state: FSMContext):
    try:
        price = int(message.text)  # проверка на число
        user_tag = message.from_user.username
        ads_id = rf.get("/get_ad_id")['ad_id']  # запрос id товара

        await state.update_data(price=price)
        await state.update_data(user_tag=user_tag)
        await state.update_data(ads_id=ads_id)
        # добавление остальной инфы

        data = await state.get_data()
        ad_message, image_id = await of.create_ad_message(data)  # создание объявления
        print(data)

        if image_id:  # проверка наличия фото
            await message.answer_photo(photo=image_id, caption=ad_message, parse_mode='Markdown',
                                       reply_markup=kb.ready_ad)
        else:
            await message.answer(ad_message, parse_mode='Markdown', reply_markup=kb.ready_ad)

        await state.set_state(None)
    except ValueError:  # работает при ошибка с преобразованием в число (строка 77)
        await message.answer("Пожалуйста, введите корректную цену (число). Попробуйте снова:")


@router.callback_query(lambda c: c.data == "publish")
async def publish(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    ad_message, image_id = await of.create_ad_message(data)
    if image_id == "":
        publish_ad = await bot.send_message(chat_id="@YL_WEB_PROJECT_TGBO", caption=ad_message, parse_mode='Markdown')
    else:
        publish_ad = await bot.send_photo(chat_id="@YL_WEB_PROJECT_TGBO",
                                          photo=image_id, caption=ad_message, parse_mode='Markdown')
    message_id = publish_ad.message_id
    print(message_id)
    data["message_id"] = message_id
    result = rf.post("/add_ad", data)
    print(result)
    await callback.answer()
    await callback.message.delete()
    if result["status"] == "OK":
        await callback.message.answer(f"Опубликовано✅\n\n[обявление]"
                                      f"(https://t.me/YL_WEB_PROJECT_TGBO/{publish_ad.message_id})",
                                      parse_mode='Markdown')
    else:
        await bot.delete_message(chat_id="@YL_WEB_PROJECT_TGBO", message_id=message_id)
        await callback.message.answer("*Произошла ошибка, попробуйте позже!*",
                                      parse_mode='Markdown')


