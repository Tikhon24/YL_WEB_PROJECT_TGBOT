from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Регестрация")]
])

without_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Без картинки", callback_data="no_image")]
])

ready_ad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
    [InlineKeyboardButton(text="Удалить", callback_data="delete")]
])