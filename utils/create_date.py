from datetime import date, datetime, timedelta


def create_date(arg_date = datetime.today(), last_month = False) -> (str, str):
	"""
	Create and get tuple of dates - (first day of month, last day of month)
	:param arg_date: Current date
	:param last_month: Data is last month
	:return: (first day of month, last day of month)
	"""
	if last_month:
		max_days = str(date(int(arg_date.year) + int(int(arg_date.month) / 12), int(arg_date.month) % 12 + 1, 1) - timedelta(days = 1)).split("-")[2]
		arg_date = arg_date - timedelta(days = int(max_days))
		
	year = int(arg_date.year)
	month = int(arg_date.month)
	last_day_of_date = str(date(year + int(month / 12), month % 12 + 1, 1) - timedelta(days = 1))
	month = str(month) if len(str(month)) == 2 else "0{}".format(str(month))
	# print(datetime.now() - timedelta(days = 30) - timedelta(days = 30))
	return "{}-{}-01 00:00:00".format(year, month), "{} 23:59:59".format(last_day_of_date)


def get_year_month(arg_date = datetime.today(), last_month = False) -> (int, int):
	year = int(arg_date.year)
	month = int(arg_date.month)
	if last_month:
		month -= 1
		if month == 0:
			year -= 1
			month = 12
	return year, month
	



if __name__ == "__main__":
	# print(create_date())
	# print(create_date(last_month = False))
	# print(create_date(last_month = True))
	print(get_year_month())
	print(get_year_month(last_month = False))
	print(get_year_month(last_month = True))