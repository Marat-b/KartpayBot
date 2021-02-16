from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('getid'))
async def get_id(message: types.Message):
	await message.answer("Mой ID: {}".format(message.from_user.id))
