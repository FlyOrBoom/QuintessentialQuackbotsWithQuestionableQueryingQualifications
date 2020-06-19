import os
import pickle
import config_

def read():
	with open(config_.read('paths','cache'),'rb') as cache:
		return pickle.load(cache) 
def write(data):
	with open(config_.read('paths','cache'),'wb') as cache:
		pickle.dump(data,cache) 
if not os.path.exists(config_.read('paths','cache')):
	write(set([]))
