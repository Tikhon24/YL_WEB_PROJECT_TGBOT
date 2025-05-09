import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
