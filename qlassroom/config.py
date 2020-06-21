import yaml
import sys
from print_fancy import *

def load():
	try:
		with open('config.yaml') as file:
			return yaml.safe_load(file)
	except yaml.YAMLError as error:
		print_warning('Invalid config.yaml.', error)
		return use_template()
	except OSError:
		return use_template()	

def read(key):
	response = load()[key]
	if key == 'channel ids' and not response:
		while True:
			try:
				channel_id = int(input('Please enter a channel ID: '))
				assert 1e17 <= channel_id < 1e18
			except KeyboardInterrupt:
				print()
				sys.exit(0)
			except:
				print_error('Not a valid channel ID.')
			else:
				write('channel ids',[channel_id])
				break
		print_success('You may enter more channel IDs at config.yaml.')
	return load()[key]

def use_template():
	try:
		with open('.config_template.yaml') as template:
			open('config.yaml','x').close()
			with open('config.yaml','w') as file:
				file.write(template.read())
				print_time('Created new config.yaml from template')
				return yaml.safe_load(file)
	except yaml.YAMLError as error:
		print_error('Invalid .config_template.yaml', error)
		return False
	except OSError as error:
		print_error('.config_template.yaml does not exist.', error)
		return False

def write(key,value):
	config = load()
	config[key] = value
	with open('config.yaml','w') as file:
		return yaml.dump(config, file)

load()

print_time('Current configuration at config.yaml:\033[96m')
with open('config.yaml') as file:
	print(file.read()[:-1]+'\033[0m')
read('channel ids')
