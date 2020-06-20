import re
import datetime

def color_ribbon(number):
	return ''.join([
		f'\033[38:5:{x}m▮'
		for x
		in re.findall('..',number)
	])

def print_time(*args):
	time = f'\033[95m{str(datetime.datetime.now()).split(" ")[1].split(".")[0]}:\033[0m'
	return print(time,*args)

def print_error(*args):
	return print_time(
		'\033[91mError:\033[0m',
		*args
	)

def print_warning(*args):
	return print_time(
		'\033[93mWarning:\033[0m',
		*args
	)
