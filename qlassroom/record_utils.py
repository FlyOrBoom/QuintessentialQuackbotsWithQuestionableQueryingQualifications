import yaml
from string_utils import *

def load():
	try:
		with open('records.yaml') as file:
			return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),warning,'Invalid records.yaml.')
		return use_template()
	except OSError:
		return use_template()	

def read(directory,key):
	return load()[directory][key]

def use_template():
	try:
		with open('.template-records.yaml') as template:
			with open('records.yaml','w') as file:
				file.write(template.read())
				print(time(),'Created new records.yaml from template')
				return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),error,'Invalid .template-records.yaml')
		return False
	except OSError:
		print(time(),error,'.template-records.yaml does not exist.')
		return False

def append(directory,key,value):
	return write(
		directory,key,
		read(directory,key).append(value)
	)

def write(directory,key,value):
	records = load()
	records[directory][key] = value
	with open('records.yaml','w') as file:
		return yaml.dump(records, file)
