from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskEditState(StatesGroup):
	PutDistance = State()
	PutActPhoto = State()
	PutUpdPhoto = State()
	PutPointPhoto = State()
