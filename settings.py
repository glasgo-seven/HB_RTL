import datetime
from types import FunctionType as function

from Citrine import console

#	----	Variables for setting up the project	----

TOKEN_FILE			:	str	=	'token'
TOKEN_FILE_DEBUG	:	str	=	'.DEBUG_token'
CHAT_ID_FILE		:	str	=	'chat_id'
CHAT_ID_FILE_DEBUG	:	str	=	'.DEBUG_chat_id'

TOKEN_ENV_VAR		:	str	=	'BOT_TOKEN'
CHAT_ID_ENV_VAR		:	str	=	'BOT_CHAT_ID'

SCHEDULE_TIMEOUT	:	int	=	5

#	NOTE when setting time
#		If selected timezone has negative difference with local timezone - the date will have an additional day!
ALERT_TIME			:	str	=	"09:00"
ALERT_TIMEZONE		:	str	=	"Europe/Moscow"

FILE_ENCODING		:	str	=	'utf-8'

BIRTHDAYS_FILE					:	str	=	'./birthdays.csv'
BIRTHDAYS_FILE_LINE_SEPARATOR	:	str	=	','
BIRTHDAYS_FILE_DATE_SEPARATOR	:	str	=	'.'

HAPPY_BIRTHDAY_MESSAGE_FILE_ONE				:	str	=	'./happy_birthday_message_one.txt'
HAPPY_BIRTHDAY_MESSAGE_FILE_MANY			:	str	=	'./happy_birthday_message_many.txt'
HAPPY_BIRTHDAY_MESSAGE_FILE_PERSON_TAG		:	str	=	'%PERSON%'


#	----	Console messages	----

CONSOLE_SYSTEM_TIME		:	function	=	lambda			:	datetime.datetime.now()

CONSOLE_NOTIFICATION_SYSTEM_TIME			:	function	=	lambda			:	console.notification(f"[NOTIFICATION]:\tSYSTEM_TIME: {CONSOLE_SYSTEM_TIME()}")
CONSOLE_NOTIFICATION_BIRTHDAYS_FOUND		:	function	=	lambda _dates	:	console.notification(f"[NOTIFICATION]:\tSending HBs to the [{' '.join(_dates)}].")
CONSOLE_NOTIFICATION_BIRTHDAYS_SEND			:	function	=	lambda			:	console.notification(f"[NOTIFICATION]:\tSuccess!")
CONSOLE_NOTIFICATION_BIRTHDAYS_NOT_FOUND	:	function	=	lambda			:	console.notification(f"[NOTIFICATION]:\tNo birthdays for today.")

CONSOLE_ALERT_NEXT_RUN		:	function	=	lambda _next_run	:	console.alert(f"[ALERT]:\tNext run on: {_next_run} SYSTEM_TIME.")
CONSOLE_ALERT_BOT_READY		:	function	=	lambda				:	console.alert(f"[ALERT]:\tI am ready to work!")
CONSOLE_ALERT_BOT_OVER		:	function	=	lambda				:	console.alert(f"[ALERT]:\tThe work is over!")
CONSOLE_ALERT_UNKNOWN_ARGV	:	function	=	lambda				:	console.alert(f"[ALERT]:\tUnknown argv ignored.")



#	----	DEBUG STATES	----

DEBUG		:	str	=	'DEBUG'
DEBUG_ALERT	:	str	=	'DEBUG_ALERT'
ENABLED		:	str	=	'ENABLED'
ALERT		:	str	=	'ALERT'

CONSOLE_ALERT_DEBUG_MODE_DEBUG			:	function	=	lambda	:	console.alert("[ALERT]:\tDEBUG MODE			:	ON")
CONSOLE_ALERT_DEBUG_MODE_DEBUG_ALERT	:	function	=	lambda	:	console.alert("[ALERT]:\tDEBUG_ALERT MODE	:	ON")


DEBUG_MODE	:	dict[str, dict]	=	{
	DEBUG		:	{
		ENABLED		:	False,
		ALERT		:	CONSOLE_ALERT_DEBUG_MODE_DEBUG
	},
	DEBUG_ALERT	:	{
		ENABLED		:	False,
		ALERT		:	CONSOLE_ALERT_DEBUG_MODE_DEBUG_ALERT
	},

}


