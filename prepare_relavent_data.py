import textPreprocess
import numpy as np
import pandas as pd
import load_relavent_data
import prepareDataset
import pickle

def build():
	#relavent_data =loadData.tweets[loadData.tweets_target == 1]
	#relavent_data = relavent_data.iloc[:,0:4]
	#print("relavent data: ", relavent_data)
	#load data
	state = load_relavent_data.tweets_state
	text = load_relavent_data.tweets_text
	label = load_relavent_data.tweets_target.reset_index(drop = True)
	#vectorize text
	text = prepareDataset.vec_text(text)
	text = pd.DataFrame(data = text, index = [i for i in range(len(text))])
	 
	#concatenate vectorized text and target
	frames = [state, text, label]
	dataset = pd.concat(frames, axis=1)
	return dataset
