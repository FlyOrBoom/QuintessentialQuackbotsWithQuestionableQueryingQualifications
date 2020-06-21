import re
from datetime import datetime
from random import randint

def color_ribbon(number):
	return ''.join([
		f'\033[38:5:{132+int(x)}m▮'
		for x
		in re.findall('..',number)
	])

def print_time(*args):
	time = f'{color_ribbon(str(randint(10,99)))} \033[95m{str(datetime.now().time())[:8]}\033[0m:'
	return print(time,*args)

def print_success(*args):
	return print_time(
		'\033[92mSuccess!\033[0m',
		*args
	)

def print_error(*args):
	return print_time(
		'\033[91mError!\033[0m',
		*args
	)

def print_warning(*args):
	return print_time(
		'\033[93mWarning!\033[0m',
		*args
	)
