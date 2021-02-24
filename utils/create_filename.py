import datetime


def create_filename(file_name: str, id_task: str, year: str = str(datetime.datetime.today().year), month: str = str(datetime.datetime.today().month), day: str = str(
		datetime.datetime.today().day)) -> str:
	template_file = "{}_{}{}{}_{}.jpg".format(file_name, year, month, day, id_task)
	return template_file
