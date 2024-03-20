#!/usr/bin/env python
# coding: utf-8

import codecs
import datetime
import os
import sys
import datetime
import time

import schedule
import telebot

from Citrine import console

from settings import *


DEBUG			:	bool	=	False
DEBUG_ALERT		:	bool	=	False


def get_token() -> str | int:
	try:
		return open(TOKEN_FILE, 'r').read()
	except FileNotFoundError:
		return os.getenv(TOKEN_ENV_VAR)
	
def get_chat_id() -> str | int:
	try:
		return open(CHAT_ID_FILE, 'r').read()
	except FileNotFoundError:
		return os.getenv(CHAT_ID_ENV_VAR)


class Bot:
	__token	:	str
	bot		:	telebot.TeleBot

	def __init__(self) -> None:
		token = get_token()
		self.__token = token
		self.bot = telebot.TeleBot(self.__token)

	def send_message(self, _chat_id: str, _message: str) -> None:
		self.bot.send_message(_chat_id, _message)


TELEGRAM_BOT	:	Bot	=	Bot()

CURRENT_YEAR	:	int	=	datetime.date.today().year

class Birthday:
	group	:	str
	date	:	datetime.date
	person	:	str
	tg_link	:	str

	def __init__(self, _birthday_line: str) -> None:
		temp_group, temp_date, temp_person, temp_tg_link = _birthday_line.split(BIRTHDAYS_FILE_LINE_SEPARATOR)
		temp_day, temp_month = [int(x) for x in temp_date.split(BIRTHDAYS_FILE_DATE_SEPARATOR)]

		self.group = temp_group
		self.date = datetime.date(CURRENT_YEAR, temp_month, temp_day)
		self.person = temp_person
		self.tg_link = temp_tg_link

	def __repr__(self) -> str:
		return f"Birthday<{self.date}, {self.person}, {self.tg_link}>"
	
	def __str__(self) -> str:
		return self.__repr__()


def load_birthdays(_file: str = BIRTHDAYS_FILE) -> list[Birthday]:
	with codecs.open(filename=_file, encoding='utf-8') as bdf:
		dates = list()
		bdf_lines = bdf.readlines()[1:]
		for line in bdf_lines:
			dates.append(Birthday(line[:-1]))
	return dates

def load_birthday_message(_file: str) -> str:
	file_size = os.stat(_file).st_size
	with codecs.open(filename=_file, encoding='utf-8') as hbm:
		message = hbm.read(file_size)
	return message


def send_happy_birthday(_dates: list[Birthday], _is_many: bool):
	if _is_many:
		message = load_birthday_message(HAPPY_BIRTHDAY_MESSAGE_FILE_MANY)

		message_half_a, message_half_b = message.split(HAPPY_BIRTHDAY_MESSAGE_FILE_PERSON_TAG)

		persons = [f"{person.person} {person.tg_link}" for person in _dates]

		message = f"{message_half_a}{' и '.join(persons)}{message_half_b}"
	else:
		_dates = _dates[0]
		message = load_birthday_message(HAPPY_BIRTHDAY_MESSAGE_FILE_ONE)

		message_half_a, message_half_b = message.split(HAPPY_BIRTHDAY_MESSAGE_FILE_PERSON_TAG)
		message = f"{message_half_a}{_dates.person} {_dates.tg_link}{message_half_b}"
	
	# print(message)
	TELEGRAM_BOT.send_message(get_chat_id(), message)


def job():
	todays_birthdays = list()
	for day in load_birthdays():
		if day.date == datetime.date.today():
			todays_birthdays.append(day)
	console.notification(f"LOCAL_TIME: {datetime.date.today()} | Sending HBs to the [{' '.join(todays_birthdays)}].")
	send_happy_birthday(todays_birthdays, len(todays_birthdays) > 1)
	console.notification("Success!")


def main():
	if DEBUG_ALERT or DEBUG:
		_job = schedule.every(SCHEDULE_TIMEOUT).seconds.do(job)
	else:
		_job = schedule.every().day.at(ALERT_TIME, ALERT_TIMEZONE).do(job)

	console.alert(f"Next run on: {_job.next_run} LOCAL_TIME.")

	is_running = True

	console.alert("I am ready to work!")
	
	while is_running:
		schedule.run_pending()
		time.sleep(SCHEDULE_TIMEOUT)

	console.alert("The work is over!")



if __name__ == '__main__':
	argv = sys.argv
	if len(argv) > 1:
		if argv[1] not in ['DEBUG', 'DEBUG_ALERT']:
			console.alert("Unknown argv ignored.")
		else:
			match argv[1]:
				case 'DEBUG':
					console.alert("DEBUG MODE : ON")
					DEBUG = True
				case 'DEBUG_ALERT':
					console.alert("DEBUG_ALERT MODE : ON")
					DEBUG_ALERT = True

		if DEBUG:
			TOKEN_FILE = TOKEN_FILE_DEBUG
			CHAT_ID_FILE = CHAT_ID_FILE_DEBUG

	main()