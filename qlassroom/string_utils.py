import re
import datetime

error = '\033[91mError:\033[0m'
warning = '\033[93mWarning:\033[0m'

def time():
	return f'\033[95m{str(datetime.datetime.now()).split(" ")[1].split(".")[0]}:\033[0m'

def color_ribbon(number):
	return ''.join([
		f'\033[38:5:{x}m▮'
		for x
		in re.findall('..',number)
	])
