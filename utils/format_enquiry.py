from aiogram.utils.markdown import bold, hcode


def format_enquiry(state_name, enquiry):
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
