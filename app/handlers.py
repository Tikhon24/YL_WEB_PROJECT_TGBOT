from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
from dotenv import load_dotenv
from create_bot import bot

import app.other_funcs as of
import app.requests_funcs as rf

import app.keyboards as kb

router = Router()

load_dotenv()

TGK_ADDRESS = os.getenv("TGK_ADDRESS")


class AddAdForm(StatesGroup):
    title = State()
    description = State()
    image = State()
    price = State()
    user_id = State()
    user_teg = State()
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
        user_id = message.from_user.id
        user_tag = message.from_user.username
        ads_id = rf.get("/get_ad_id")['ad_id']  # запрос id товара

        await state.update_data(price=price)
        await state.update_data(user_id=user_id)
        await state.update_data(user_tag=user_tag)
        await state.update_data(ads_id=ads_id)
        # добавление остальной инфы

        data = await state.get_data()
        ad_message, image_id = await of.create_ad_message(data)  # создание объявления

        if image_id:  # проверка наличия фото
            await message.answer_photo(photo=image_id, caption=ad_message, parse_mode='Markdown',
                                       reply_markup=kb.ready_ad)
        else:
            await message.answer(ad_message, parse_mode='Markdown', reply_markup=kb.ready_ad)

        await state.set_state(None)
    except ValueError:  # работает при ошибка с преобразованием в число (строка 84)
        await message.answer("Пожалуйста, введите корректную цену (число). Попробуйте снова:")
    except TypeError:
        await message.answer("*Произошла ошибка, попробуйте позже!*",
                             parse_mode='Markdown')


@router.callback_query(lambda c: c.data == "publish")
async def publish(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        ad_message, image_id = await of.create_ad_message(data)
        if image_id == "":
            publish_ad = await bot.send_message(chat_id=f"@{TGK_ADDRESS}", text=ad_message, parse_mode='Markdown')
        else:
            publish_ad = await bot.send_photo(chat_id=f"@{TGK_ADDRESS}",
                                              photo=image_id, caption=ad_message, parse_mode='Markdown')
        message_id = publish_ad.message_id
        data["message_id"] = message_id
        result = rf.post("/add_ad", data)
        await callback.answer()
        await callback.message.delete()
        if result["status"] == "ERROR":
            raise ValueError("Ошибка записи объявления в бд")
        await callback.message.answer(f"Опубликовано✅\n\n[объявление]"
                                      f"(https://t.me/{TGK_ADDRESS}/{publish_ad.message_id})",
                                      parse_mode='Markdown')
    except Exception as e:
        print(f"ОШИБКА: {e}")
        await bot.delete_message(chat_id="@YL_WEB_PROJECT_TGBO", message_id=message_id)
        await callback.message.answer("*Произошла ошибка, попробуйте позже!*",
                                      parse_mode='Markdown')


@router.message(Command("my_ads"))
async def show_ads(message: Message) -> None:
    user_id = message.from_user.id
    ads = rf.get(f"/get_ad/user_id", params={'value': f'{user_id}'})
    if ads["status"] == "OK":
        kb_ads = InlineKeyboardMarkup(inline_keyboard=[])
        for ad in ads['ads']:
            kb_ads.inline_keyboard.append(
                [InlineKeyboardButton(text=ad["title"], callback_data=f"click_ad:{ad['ads_id']}")])
        await message.answer("*Ваши ады*", reply_markup=kb_ads)
    elif ads["status"] == "ERROR":
        pass


@router.callback_query(lambda c: c.data.startswith('click_ad:'))
async def process_callback_button(callback: CallbackQuery):
    data = callback.data.split(':')
    ad_id = data[1]  # Получаем дополнительную информацию
    print(ad_id)
    ad = rf.get(f"/get_ad/ads_id/{ad_id}")
    print(ad)
    ad_message, image_id = await of.create_ad_message(ad)
    print(ad_message)
    await callback.answer()

    if image_id:  # проверка наличия фото
        await callback.message.answer_photo(photo=image_id, caption=ad_message, parse_mode='Markdown')
    else:
        await callback.message.answer(ad_message, parse_mode='Markdown')
