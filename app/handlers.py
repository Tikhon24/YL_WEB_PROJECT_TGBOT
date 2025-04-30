from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("*старт*", reply_markup=kb.start)


@router.message(Command("help"))
async def get_help(message: Message) -> None:
    await message.answer("*помощь*")


@router.message(F.text == "лох")
async def lox(message: Message) -> None:
    await message.answer("сам лох")