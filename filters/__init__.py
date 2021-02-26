from aiogram import Dispatcher

# from loader import dp
from .member import IsMember


# if __name__ == "filters":
def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsMember)
    pass
