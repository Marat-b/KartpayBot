from aiogram.utils.markdown import bold, hcode


def format_enquiry(enquiry):
	if len(enquiry) == 0:
		return "Данных нет"
	formatted_enquiry = [
		'<code>Заявка со статусом:</code> <i>{}</i>'.format(enquiry['f78321']),
		'',
		'<i>Номер заявки: {}</i>'.format(enquiry["id"]),
		'Клиент: <b>{}</b>'.format(enquiry['f78201']),
		'Адрес: {}'.format(enquiry['f78211']),
		'Телефон: {}'.format(enquiry['f78341']),
		'Дата исполнения: {}'.format(hcode(enquiry['f78311'])),
		'Срок установки: {}'.format(hcode(enquiry['f81181'])),
		'Доставка: {}'.format(enquiry['f79841'])
	]
	return '\n'.join(formatted_enquiry)


def format_enquiry_for_paying(enquiry):
	if len(enquiry) == 0:
		return "Данных нет"
	formatted_enquiry_for_paying = [
		'<code>Заявка со статусом:</code> <i>{}</i>'.format(enquiry['f78321']),
		'',
		'<i>Номер заявки: {}</i>'.format(enquiry["id"]),
		'Клиент: <b>{}</b>'.format(enquiry['f78201']),
		'Адрес: {}'.format(enquiry['f78211']),
		'Дата исполнения: {}'.format(hcode(enquiry['f78311'])),
		'Срок установки: {}'.format(hcode(enquiry['f81181'])),
		"Пробег: {}  км".format(enquiry["f78361"]),
		"Акт по заявке: {}".format("Да" if len(str(enquiry["f81381"]).strip()) > 0 else "Нет"),
		"УПД по заявке: {}".format("Да" if len(str(enquiry["f81301"]).strip()) > 0 else "Нет"),
		"Заявка оплачена: {}".format(enquiry["f81311"]),
		"Вознаграждение по заявке: {} руб".format(enquiry["f81291"])
		# 'Телефон: {}'.format(enquiry['f78341']),
		# 'Доставка: {}'.format(enquiry['f79841'])
	]
	return '\n'.join(formatted_enquiry_for_paying)
