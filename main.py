#!/usr/bin/python3.6
from datetime import timedelta, datetime
import os
import shutil
import time


now = datetime.now()  # узнаём текущую дату
now_year = now.strftime("%Y")  # формат str, форматируем, беря только год
int_now_year = int(now_year)  # переводим str в int
last_year = int_now_year - 1  # "вычисляем" прошлый год
str_last_year = str(last_year)  # переводим обратно int в str

week = timedelta(7)  # берём дельту в 7 дней (неделя)
up_to_week = now - week  # от текущей даты отнимаем неделю
str_up_to_week = up_to_week.strftime("%Y")  # формат str, форматируем дату недельной давности, берём только год


main_path = '/var/spool/asterisk/monitor/'  # основная директория без учёта года


# главная функция, которая дёргает все остальные
def main():
	check_for_year(os.path.join(main_path + str_last_year), 5)  # функция по проверке и чистки прошлого года, как аргумент передаём путь и количество дней (5) которое оставить
	del_last_year_folder(os.path.join(main_path + str_last_year))  # функция по сверке времени и если текущий год > прошлого года, то удаляет прошлогоднюю папку
	check_for_year(os.path.join(main_path + now_year),4)  # функция по проверке и чистки прошлого года, как аргумент передаём путь и количество дней (4) которое оставить


def del_last_year_folder(path):
	if now_year > str_up_to_week:
		if os.path.exists(path):
			try:
				shutil.rmtree(path)
			except OSError as e:
				print("Error: %s : %s" % (path, e.strerror))
		else:
			print('Directory or files no find')
	else:
		print('Not ure year, buddy :(')


def check_for_year(path, days):
	seconds = time.time() - (days * 24 * 60 * 60)
	if os.path.exists(path):
		for root_folder, folders, files in os.walk(path):
			if seconds >= get_file_or_folder_age(root_folder):
				remove_folder(root_folder)
				break
			else:
				for folder in folders:
					folder_path = os.path.join(root_folder, folder)
					if seconds >= get_file_or_folder_age(folder_path):
						remove_folder(folder_path)
				for file in files:
					file_path = os.path.join(root_folder, file)
					if seconds >= get_file_or_folder_age(file_path):
						remove_file(file_path)
		else:
			if seconds >= get_file_or_folder_age(path):
				remove_file(path)
	else:
		print(f"{path} is not found, no files & folders deleted")


def remove_folder(path):
	if not shutil.rmtree(path):
		print(f"{path} is removed successfully")
	else:
		print(f"Unable to delete the {path}")


def remove_file(path):
	if not os.remove(path):
		print(f"{path} is removed successfully")
	else:
		print(f"Unable to delete the {path}")


def get_file_or_folder_age(path):
	ctime = os.stat(path).st_ctime
	return ctime


if __name__ == '__main__':
	main()
