from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery

# from filters import IsMember
from keyboards.inline.inline_type_request_menu import inline_type_request_menu
from keyboards.main_menu import main_menu
from keyboards.inline.choice_request_buttons import choice_request
from keyboards.requests_menu import requests_menu
from loader import dp
from data import config, access_id
from states.task_close_inquire_state import TaskCloseInquiryState
from utils.choice_request_buttons import choice_request_buttons


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
	await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup = main_menu, disable_notification = True)


@dp.message_handler(regexp = "Мои заявки")
async def keyboard_start(message: types.Message):
	# await message.delete()
	# await message.answer("Выберите тип заявки", reply_markup = inline_type_request_menu(), disable_notification = True)
	await choice_request_buttons(message)


@dp.callback_query_handler(text = "back", state = [TaskCloseInquiryState.PutActPhoto, TaskCloseInquiryState.PutUpdPhoto])
async def keyboard_start(call: CallbackQuery, state: FSMContext):
	await state.finish()
	await choice_request_buttons(call.message)
