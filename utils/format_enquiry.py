from aiogram.utils.markdown import bold, hcode


def format_enquiry(enquiry):
	formatted_enquiry = [
		'<i>Номер заявки: {}</i>'.format(enquiry["id"]),
		'Клиент: <b>{}</b>'.format(enquiry['f78201']),
		'Адрес: {}'.format(enquiry['f78211']),
		'Телефон: {}'.format(enquiry['f78341']),
		'Срок установки: {}'.format(hcode(enquiry['f81181']))
	]
	return '\n'.join(formatted_enquiry)
