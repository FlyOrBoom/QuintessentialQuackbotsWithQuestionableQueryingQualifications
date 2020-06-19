import os
import pickle
import config 

path = '.cache.pickle'

def read():
	if not os.path.exists(path):
		write(set())
	with open(path,'rb') as cache:
		return pickle.load(cache) 
def write(data):
	with open(path,'wb') as cache:
		return pickle.dump(data,cache) 
