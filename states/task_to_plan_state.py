from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskToPlanState(StatesGroup):
	PutDate = State()
