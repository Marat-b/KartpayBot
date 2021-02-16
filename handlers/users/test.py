from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from telegram_bot_pagination import InlineKeyboardPaginator

from loader import dp

data = ["Q", "A", "Z", "W", "S", "X", "E", "D", "C", "R", "F", "V"]

class TestState(StatesGroup):
	TestState = State()

@dp.message_handler(Command("test"))
async def test(message: types.Message, state: FSMContext):
	paginator = InlineKeyboardPaginator(
			len(data),
			current_page = 0,
			data_pattern = 'page#{page}'
	)
	# await TestState.TestState.set()
	await state.update_data(test_state = "Test_State")
	
	await message.answer(data[0], reply_markup = paginator.markup)


@dp.callback_query_handler(regexp = 'page\#\d')
async def callback_test(call: CallbackQuery, state: FSMContext):
	print(f'-> {call.data}')
	page = call.data.split('#')[1]
	print(f'page={str(page)}')
	
	# await call.message.answer(call.message.text)
	paginator = InlineKeyboardPaginator(
			len(data),
			current_page = int(page),
			data_pattern = 'page#{page}'
	)
	await call.message.edit_text(data[int(page) - 1], reply_markup = paginator.markup)
	data_state = await state.get_data()
	test_data = data_state.get("test_state")
	print(f"test_data = {test_data}")
