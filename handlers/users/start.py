from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from filters import IsMember
from keyboards.inline.choice_request_buttons import choice_request
from loader import dp
from data import config, access_id


@dp.message_handler(IsMember(), CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Выберите тип заявки:", reply_markup = choice_request())
