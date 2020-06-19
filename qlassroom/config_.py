import yaml
from string_ import *

def load():
	try:
		with open('config.yaml') as file:
			return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),warning,'Invalid config.yaml.')
		return use_template()
	except OSError:
		return use_template()	

def read(directory,key):
	return load()[directory][key]

def use_template():
	try:
		with open('.template-config.yaml') as template:
			with open('config.yaml','w') as file:
				file.write(template.read())
				print(time(),'Created new config.yaml from template')
				return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),error,'Invalid .template-config.yaml')
		return False
	except OSError:
		print(time(),error,'.template-config.yaml does not exist.')
		return False

def append(directory,key,value):
	return write(
		directory,key,
		read(directory,key).append(value)
	)

def write(directory,key,value):
	config = load()
	config[directory][key] = value
	with open('config.yaml','w') as file:
		return yaml.dump(config, file)
