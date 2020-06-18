import re
def color_ribbon(number):
	return ''.join(
		f'\033[38:5:{x}m▮'
		for x
		in re.findall('..',number)
	)

print(''.join([1234545,100]))
