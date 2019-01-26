# Self written class
import construct_model
import load_relavent_data
import prepareDataset
import textPreprocess
import trainModel
import dictionary

#Import Library
import tensorflow as tf
import h5py
import pandas as pd
import pickle
import numpy as np
import math
import random
from itertools import permutations
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.neural_network import MLPClassifier
#plot library
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

units = trainModel.units
def text2int(test):
	# load dictionary that maps string to its ID
	text2int = dictionary.load_dictionary()

	# preprocess text and convert given text to vector
	preprocess_text = textPreprocess.preprocess(test)
	print("text", preprocess_text)
	vect_texts = np.zeros(shape = (1, len(text2int)))
	for word in preprocess_text.split():
		if word in text2int:
			vect_texts[0][text2int[word]] += 1
		else:
			vect_texts[0][0] += 1 # set to unknown
	print("%Unknkown",vect_texts[0][0]/len(preprocess_text.split()))
	return vect_texts

def relavent(string):
	dataset = prepareDataset.build_r_nr().sample(frac = 1)
	input_shape = dataset.shape[1]-1
	# save memory
	del dataset
	# reload tensorflow keras model to fit
	model = construct_model.sigmoid_clip(units, input_shape)
	model.load_weights("tweet_weight.hdf5", by_name = False)
	string_as_int = text2int(string.lower())
	#output prediction
	predictions = model.predict(string_as_int, batch_size=1)
	print("relavence",predictions)
	if round(predictions[0][0]*10)/10 >= 0.3:
		return 1
	else:
		return 0

def bull_bear(string):
	dataset = prepareDataset.build_bull_bear().sample(frac=1)
	input_shape = dataset.shape[1]-1
	# save memory
	del dataset
	# reload tensorflow keras model
	model = construct_model.sigmoid_clip(units, input_shape)
	model.load_weights("bull_bear_weight.hdf5", by_name = False)
	string_as_int = text2int(string.lower())
	# output prediction
	predictions = model.predict(string_as_int, batch_size=1)
	print("%bull",predictions)
	if round(predictions[0][0]*10)/10 >= 0.5:
		return 1
	else:
		return 0

def stock_quote(test):
	#prediction
	print("**********************Predict**************************")
	mlpreg = None
	with open('candle_analysis_model.pkl', 'rb') as f:
		mlpreg = pickle.load(f)
	test_prediction = mlpreg.predict(test)
	# save memory
	del mlpreg
	print("test prediction: ", test_prediction)
	return test_prediction

def tweet_score(take):
	# take most receint 'take' tweets
	bullish_tweets = load_relavent_data.tweets[load_relavent_data.tweets_target == 1].iloc[take:,:]
	bearish_tweets = load_relavent_data.tweets[load_relavent_data.tweets_target == 0].iloc[take:,:]
	# number of bullish tweet and bearish tweets
	num_bullish = bullish_tweets.shape[0]
	num_bearish = bearish_tweets.shape[0]
	# strength base on number of bullish/bearish tweets
	bullish_strength = bullish_tweets.iloc[:, 1:3].sum().sum()
	bearish_strength = bearish_tweets.iloc[:, 1:3].sum().sum()
	# save memory
	del bullish_tweets
	del bearish_tweets
	# compute scores
	bullish_score = num_bullish*0.8 + bullish_strength * 0.2
	bearish_score = num_bearish * 0.8 + bearish_strength * 0.2
	return bullish_score / (bullish_score + bearish_score)
