import datetime


def create_filename(file_name: str, id_task: str, year: str = str(datetime.datetime.today().year), month: str = str(datetime.datetime.today().month), day: str = str(
		datetime.datetime.today().day)) -> str:
	month = month if len(month) == 2 else "0{}".format(month)
	day = day if len(day) == 2 else "0{}".format(day)
	template_file = "{}_{}{}{}_{}.jpg".format(file_name, year, month, day, id_task)
	return template_file
