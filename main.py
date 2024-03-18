#!/usr/bin/env python
# coding: utf-8

import codecs
import datetime
import os
import sys
import time

import schedule
import telebot

from Citrine import console


DEBUG			:	bool	=	False

TOKEN_FILE			:	str		=	'token'
TOKEN_FILE_DEBUG	:	str		=	'.DEBUG_token'
CHAT_ID_FILE		:	str		=	'chat_id'
CHAT_ID_FILE_DEBUG	:	str		=	'.DEBUG_chat_id'


def get_token() -> str | int:
	try:
		return open(TOKEN_FILE, 'r').read()
	except FileNotFoundError:
		return os.getenv('BOT_TOKEN')
	
def get_chat_id() -> str | int:
	try:
		return open(CHAT_ID_FILE, 'r').read()
	except FileNotFoundError:
		return os.getenv('BOT_CHAT_ID')


class Bot:
	__token	:	str
	bot		:	telebot.TeleBot

	def __init__(self) -> None:
		self.__token = get_token()
		self.bot = telebot.TeleBot(self.__token)

	def send_message(self, _chat_id: str, _message: str) -> None:
		self.bot.send_message(_chat_id, _message)


TELEGRAM_BOT	:	Bot

CURRENT_YEAR		:	int	=	datetime.date.today().year
SCHEDULE_TIMEOUT	:	int =	5

BIRTHDAYS_FILE					:	str	=	'./birthdays.csv'
BIRTHDAYS_FILE_LINE_SEPARATOR	:	str	=	','
BIRTHDAYS_FILE_DATE_SEPARATOR	:	str	=	'.'

HAPPY_BIRTHDAY_MESSAGE_FILE_ONE				:	str	=	'./happy_birthday_message_one.txt'
HAPPY_BIRTHDAY_MESSAGE_FILE_MANY			:	str	=	'./happy_birthday_message_many.txt'
HAPPY_BIRTHDAY_MESSAGE_FILE_PERSON_TAG		:	str	=	'%PERSON%'


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
	send_happy_birthday(todays_birthdays, len(todays_birthdays) > 1)


def main():
	if DEBUG:
		schedule.every(5).seconds.do(job)
	else:
		schedule.every().day.at("08:50", "Europe/Moscow").do(job)

	is_running = True

	console.alert("I am ready to work!")
	while is_running:
		schedule.run_pending()
		time.sleep(SCHEDULE_TIMEOUT)



if __name__ == '__main__':
	argv = sys.argv
	if len(argv) > 1:
		if argv[1]!='DEBUG':
			console.alert("Unknown argv ignored.")
		else:
			console.alert("DEBUG MODE : ON")
			DEBUG = True
		
		if DEBUG:
			TOKEN_FILE = TOKEN_FILE_DEBUG
			CHAT_ID_FILE = CHAT_ID_FILE_DEBUG

		TELEGRAM_BOT = Bot()

	main()