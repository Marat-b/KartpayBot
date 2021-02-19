import yadisk
import requests

from data import config


class CloudStorage:
	
	@classmethod
	def save_file(cls, source_file, destination_file):
		storage = yadisk.YaDisk(token = config.YANDEX_TOKEN)
		telegram_file_path = config.TELEGRAM_FILE_PATH
		cloud_file_path = config.CLOUD_FILE_PATH
		cloud_public_file_path = config.CLOUD_PUBLIC_FILE_PATH
		file_name = destination_file.split("/")[-1]
		
		url = str(telegram_file_path).format(source_file)
		request = requests.get(url)
		with open("temp_file.jpg", "wb") as f:
			f.write(request.content)
		
		# storage.upload(str(telegram_file_path).format(source_file), str(cloud_file_path).format(file_name))
		# storage.upload(source_file, str(cloud_file_path).format(file_name), overwrite=True)
		storage.upload("temp_file.jpg", str(cloud_file_path).format(file_name), overwrite = True)
		is_saved = storage.exists(str(cloud_file_path).format(file_name))
		if is_saved:
			return str(cloud_public_file_path).format(file_name), is_saved
		else:
			return "", is_saved


if __name__ == "__main__":
	file_path, is_saved = CloudStorage.save_file("C:\\softz\\file_40.jpg", "/Kartpay/file_40.jpg")
	
	if is_saved:
		print(f"file exists = {file_path}")
	else:
		print("file NOT exists")
