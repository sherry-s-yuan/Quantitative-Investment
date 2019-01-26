# build dictionary {'word' : id} #
import pandas as pd
import numpy as np
import loadData
import textPreprocess
import pickle
from bs4 import BeautifulSoup
import sqlite3
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen

# builds histogram for #time of appearance of a word 
def histogram(text):
	vocab = {"UNK" : 0}
	row = 1
	for i in range(text.shape[0]):
		string = textPreprocess.preprocess(text.iloc[i])
		for word in string.split():
			vocab.setdefault(word, 0)
			vocab[word] += 1
		row+=1
	return vocab

# map words to its id
def build():
	# load
	text = loadData.tweets_text
	#text = text.dropna(how = 'any').unique()

	# build histogram
	hist = histogram(text)
	del text
	# transform histogram to word:id
	text2int = hist.copy()
	#int2text = dict()
	for (i, (k,v)) in enumerate(text2int.items()):
		text2int[k] = i
		#int2text.setdefault(i, k)

	# store dictionary in file
	save_dictionary(text2int)

def expand_by_spidering(paragraph):
	# load dictionary
	text2int = load_dictionary()

	added = False
	# put new met word into dictionary
	for word in paragraph.split():
		if word not in text2int:
			for _ in range(2):
				for symbol in ['.', ',',':','!','?','"']:
					if symbol in word:
						pos = word.rfind(symbol)
						if(pos == len(word)-1):
							word = word[:pos]
						else:
							word = word[:pos]+word[pos+1:]
			print("Expand: ", word)
			size = len(text2int)
			text2int.setdefault(word, size)
			added = True
	# save dictionary
	save_dictionary(text2int)
	if added:
		return True
	else:
		return False

#expand_spider()
def load_dictionary():
	text2int = None
	with open('text2int.pkl', 'rb') as f:
		text2int = pickle.load(f)
	return text2int

def save_dictionary(text2int):
	with open('text2int.pkl', 'wb') as f:
		pickle.dump(text2int, f, pickle.HIGHEST_PROTOCOL)
