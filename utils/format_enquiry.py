from aiogram.utils.markdown import bold, hcode

from data.config import f_act_photo, f_app_description, f_client, f_client_bank, f_delivery, f_execution_date, f_id, \
	f_mileage, \
	f_paid_to_performer, \
	f_phone, f_point_address, \
	f_status, \
	f_target_date, f_upd_photo, f_work_type


def format_enquiry(enquiry):
	"""
	Formatted message about inquiry
	:param enquiry: enquiry
	:return: formatted message
	"""
	if len(enquiry) == 0:
		return "Данных нет"
	formatted_enquiry = [
		'<code>Заявка со статусом:</code> <i>{}</i>'.format(enquiry[f_status]),
		'',
		'<i>Номер заявки: {}</i>'.format(enquiry[f_id]),
		'Клиент: <b>{}</b>'.format(enquiry[f_client]),
		'Адрес: {}'.format(enquiry[f_point_address]),
		'Телефон: {}'.format(enquiry[f_phone]),
		'Банк заказчик: {}'.format(enquiry[f_client_bank]),
		'Тип работ: {}'.format(enquiry[f_work_type]),
		'Описание заявки: {}'.format(enquiry[f_app_description]),
		'Дата исполнения: {}'.format(hcode(enquiry[f_execution_date])),
		'Срок установки: {}'.format(hcode(enquiry[f_target_date])),
		'Доставка: {}'.format(enquiry[f_delivery])
	]
	return '\n'.join(formatted_enquiry)


def format_enquiry_for_paying(enquiry):
	"""
		Formatted message about inquiry
		:param enquiry: enquiry
		:return: formatted message
		"""
	if len(enquiry) == 0:
		return "Данных нет"
	formatted_enquiry_for_paying = [
		'<code>Заявка со статусом:</code> <i>{}</i>'.format(enquiry[f_status]),
		'',
		'<i>Номер заявки: {}</i>'.format(enquiry[f_id]),
		'Клиент: <b>{}</b>'.format(enquiry[f_client]),
		'Адрес: {}'.format(enquiry[f_point_address]),
		'Банк заказчик: {}'.format(enquiry[f_client_bank]),
		'Тип работ: {}'.format(enquiry[f_work_type]),
		'Описание заявки: {}'.format(enquiry[f_app_description]),
		'Дата исполнения: {}'.format(hcode(enquiry[f_execution_date])),
		'Срок установки: {}'.format(hcode(enquiry[f_target_date])),
		"Пробег: {}  км".format(enquiry[f_mileage]),
		"Акт по заявке: {}".format("Да" if len(str(enquiry[f_act_photo]).strip()) > 0 else "Нет"),
		"УПД по заявке: {}".format("Да" if len(str(enquiry[f_upd_photo]).strip()) > 0 else "Нет"),
		"Заявка оплачена: {}".format(enquiry[f_paid_to_performer]),
		# "Вознаграждение по заявке: {} руб".format(enquiry["f81291"])
		# 'Телефон: {}'.format(enquiry[f_phone]),
		# 'Доставка: {}'.format(enquiry[f_delivery])
	]
	return '\n'.join(formatted_enquiry_for_paying)
