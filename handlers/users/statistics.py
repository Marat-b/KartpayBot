from aiogram.types import Message
from aiogram.utils.emoji import emojize

from data.config import STATUS_SETUP, STATUS_UPD_SIGNED
from data.enquiry import Enquiry
from keyboards.main_menu import main_menu
from keyboards.statistics_menu import statistics_menu
from loader import dp
from utils.create_date import create_date


@dp.message_handler(regexp = "Статистика")
async def statistics_current_month(message: Message):
	await statistics(message)


@dp.message_handler(regexp = "Текущий месяц")
async def statistics_current_month(message: Message):
	await statistics(message)


@dp.message_handler(regexp = "Предыдущий месяц")
async def statistics_current_month(message: Message):
	await statistics(message, last_month = True)


@dp.message_handler(regexp = "Назад")
async def statistics_current_month(message: Message):
	await message.delete()
	await message.answer("{}  Назад".format(emojize(":leftwards_arrow_with_hook:")), reply_markup = main_menu)


async def statistics(message: Message, last_month = False):
	# print(f"statistics_current_month -> {message.from_user.id}")
	# await message.delete()
	enquiry = Enquiry(message.from_user.id)
	first_date, end_date = create_date(last_month = last_month)
	count_setup_status = len(enquiry.get_entities_for_statistics(STATUS_SETUP, first_date, end_date))
	# print('Заявок со статусом "Установлено" {} шт.'.format(count_setup_status))
	entities = enquiry.get_entities_for_statistics(STATUS_UPD_SIGNED, first_date, end_date)
	amount = 0
	count = 0
	for entity in entities:
		amount += int(entity["f81291"])
		count += 1
	# print('Заявок со статусом "УПД подписано" {} шт., на общую сумму {} руб.'.format(count, amount))
	entities = enquiry.get_entities_for_payed(first_date, end_date)
	payed_amount = 0
	payed_count = 0
	for entity in entities:
		payed_amount += int(entity["f81291"])
		payed_count += 1
	strings = ['{}  Заявок со статусом "Установлено" - <b>{}</b> шт.'.format(emojize(":one:"), count_setup_status),
	           '{}  Заявок со статусом "УПД подписано" - <b>{}</b> шт., на общую сумму - <b>{}</b> руб.'.format(emojize(":two:"), count, amount),
	           '{}  Оплачено всего <b>{}</b> заявок на сумму <b>{}</b> руб.'.format(emojize(":three:"), payed_count, payed_amount)
	           ]
	# if last_month:
	# 	strings.insert(0, "<b>Предыдущий месяц</b>")
	# else:
	# 	strings.insert(0, "<b>Текущий месяц</b>")
	await message.answer("\n".join(strings), reply_markup = statistics_menu)
