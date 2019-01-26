import textPreprocess
import numpy as np
import pandas as pd
import loadData
import pickle
import load_relavent_data
import dictionary

def build_r_nr():
	text = loadData.tweets_text
	data = vec_text(text)
	vectorized_text = pd.DataFrame(data = data, index = [i for i in range(len(data))])
	#concatenate vectorized text and target
	label = loadData.tweets_target.dropna(how = 'any').reset_index(drop = True)
	frames = [vectorized_text, label]
	dataset = pd.concat(frames, axis=1)
	return dataset

def build_bull_bear():
	#relavent_data =loadData.tweets[loadData.tweets_target == 1]
	#relavent_data = relavent_data.iloc[:,0:4]
	#print("relavent data: ", relavent_data)
	#load data
	state = load_relavent_data.tweets_state
	text = load_relavent_data.tweets_text
	label = load_relavent_data.tweets_target.reset_index(drop = True)
	#vectorize text
	text = vec_text(text)
	text = pd.DataFrame(data = text, index = [i for i in range(len(text))])
	 
	#concatenate vectorized text and target
	#frames = [state, text, label]
	frames = [text, label]
	dataset = pd.concat(frames, axis=1)
	return dataset

#convert string to vector
def vec_text(text):
	text2int = dictionary.load_dictionary()
	vect_texts = np.zeros(shape = (text.shape[0], len(text2int)))
	for i, string in enumerate(text):
		for word in textPreprocess.preprocess(string).split():
			if word in text2int:
				vect_texts[i][text2int[word]] += 1
			else:
				vect_texts[i][0] += 1 # set to unknown
	return vect_texts



