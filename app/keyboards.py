from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Регестрация")]
])

without_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Без картинки", allback_data="no_image")]
])
