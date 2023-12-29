from datetime import datetime

from aiogram.types import Message
from aiogram.utils.emoji import emojize

from data.config import STATUS_SETUP, STATUS_UPD_SIGNED, f_application_total, f_execution_date
from data.enquiry import Enquiry
from keyboards.main_menu import main_menu
from keyboards.statistics_menu import statistics_menu
from loader import dp
from utils.create_date import create_date, get_year_month


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
	# print(f"statistics_current_month -> last_month = {last_month}")
	# await message.delete()
	print(f'message={message}')
	print(f'message.from_user.id={message.from_user.id}')
	enquiry = Enquiry(message.from_user.id)
	# first_date, end_date = create_date(last_month = last_month)
	count_setup_status = len(get_records(enquiry.get_entities_for_statistics(STATUS_SETUP), last_month = last_month))
	# print('Заявок со статусом "Установлено" {} шт.'.format(count_setup_status))
	entities = get_records(enquiry.get_entities_for_statistics(STATUS_UPD_SIGNED), last_month = last_month)
	amount = 0
	count = 0
	for entity in entities:
		amount += int(entity[f_application_total])
		count += 1
	# print('Заявок со статусом "УПД подписано" {} шт., на общую сумму {} руб.'.format(count, amount))
	entities = get_records(enquiry.get_entities_for_payed(), last_month = last_month)
	payed_amount = 0
	payed_count = 0
	for entity in entities:
		payed_amount += int(entity[f_application_total])
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


def get_records(records, last_month = False):
	year, month = get_year_month(last_month = last_month)
	ret_records = []
	print(f'~records={records}')
	for record in records:
		field_date = datetime.fromisoformat(record[f_execution_date])
		if field_date.year == year and field_date.month == month:
			ret_records.append(record)
	return ret_records
