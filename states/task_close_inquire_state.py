from aiogram.dispatcher.filters.state import StatesGroup, State


class TaskCloseInquiryState(StatesGroup):
	PutDate = State()
	PutDistance = State()
	PutActPhoto = State()
	PutUpdPhoto = State()
