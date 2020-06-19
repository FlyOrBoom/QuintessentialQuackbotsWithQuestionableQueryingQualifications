import yaml
from string_utils import *

def load():
	try:
		with open('records.yaml') as file:
			return yaml.safe_load(file)
	except yaml.YAMLError:
		print(time(),warning,'Invalid records.yaml.')
		use_template_records()
		pass
	except OSError:
		use_template_records()	
		pass

def use_template_records():
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

def save(records):
	with open('records.yaml','w') as file:
		return yaml.dump(records, file)
