import yaml
from prefixes import *

def load():
	try:
		with open('config.yaml') as file:
			return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),warning,'Invalid config.yaml.')
		return use_template()
	except OSError:
		return use_template()	

def read(key):
	return load()[key]

def use_template():
	try:
		with open('.config_template.yaml') as template:
			with open('config.yaml','w') as file:
				file.write(template.read())
				print(time(),'Created new config.yaml from template')
				return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),error,'Invalid .config_template.yaml')
		return False
	except OSError:
		print(time(),error,'.config_template.yaml does not exist.')
		return False

def write(directory,key):
	config = load()
	config[key] = value
	with open('config.yaml','w') as file:
		return yaml.dump(config, file)
