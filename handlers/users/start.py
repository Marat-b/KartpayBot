from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

# from filters import IsMember
from keyboards.choice_request_kb import request_kb
from keyboards.inline.choice_request_buttons import choice_request
from loader import dp
from data import config, access_id


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
	# await message.answer(f"Привет, {message.from_user.full_name}!")
	# await message.answer("Выберите тип заявки:", reply_markup = choice_request())
	await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup = request_kb, disable_notification = True)


@dp.message_handler(text = "Начать работу")
async def keyboard_start(message: types.Message):
	await message.delete()
	await message.answer("Выберите тип заявки", reply_markup = choice_request(), disable_notification = True)
