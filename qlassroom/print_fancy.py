import re
from datetime import datetime

def color_ribbon(number):
	return ''.join([
		f'\033[38:5:{132+int(x)}m▮'
		for x
		in re.findall('..',number)
	])

def print_time(*args):
	now = str(datetime.now().time())[:8]
	time = f'\033[95m{now} {color_ribbon(now[6:])}\033[0m'
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
