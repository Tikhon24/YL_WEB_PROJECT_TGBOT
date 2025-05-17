from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/help")]
],
    resize_keyboard=True, one_time_keyboard=True
)

commands = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/add_ad")],
    [KeyboardButton(text="/my_ads")]
],
    resize_keyboard=True
)

without_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Без картинки", callback_data="no_image")]
])

ready_ad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
    [InlineKeyboardButton(text="Удалить", callback_data="delete")]
])
