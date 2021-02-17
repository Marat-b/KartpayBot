from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskDoneState(StatesGroup):
	PutDate = State()
	PutDistance = State()
	PutPhoto = State()