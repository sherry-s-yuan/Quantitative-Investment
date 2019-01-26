# train neural network with TensorFlow and keras backend

# custom class
import prepareDataset
import dictionary
import construct_model
# reference library
import tensorflow as tf
import pandas as pd
import numpy as np
from keras.backend.tensorflow_backend import clip
from keras import backend
import h5py
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score
import pickle

#dictionary.build()

# shuffle
BATCH_SIZE = 5


#dataset.groupby(np.arange(len(dataset))//10)
#for batch,data in dataset.groupby(np.arange(len(dataset))//BATCH_SIZE):
#	inp = data.iloc[:,:-1]
#	target = data.iloc[:,-1]
#	print(inp)

# INITIALIZATION
#vocab_size = dataset.shape[1]-1 # length of vocabulary
units = 60 # number of neurons per activation layer
#input_shape = len(dictionary.load_dictionary())-1


def r_nr():
	#dataset
	r_nr_data = prepareDataset.build_r_nr().sample(frac = 1)

	# train model
	input_shape = r_nr_data.shape[1]-1
	model = construct_model.sigmoid_clip(units, input_shape)
	model.fit(r_nr_data.iloc[:,:-1], r_nr_data.iloc[:,-1], epochs=8, batch_size=BATCH_SIZE)
	model.save('tweet_model.model')
	model.save_weights("tweet_weight.hdf5", overwrite=True)
	#test = 'buy bull aapl stock'
	#test_model.relavent(test)
	#new_model = tf.keras.models.load_model('tweet_model.model')

def bull_bear():
	#dataset
	bull_bear_data = prepareDataset.build_bull_bear().sample(frac=1)
	input_shape = bull_bear_data.shape[1]-1
	model = construct_model.sigmoid_clip(units, input_shape)
	# train model
	model.fit(bull_bear_data.iloc[:,:-1], bull_bear_data.iloc[:,-1], epochs=8, batch_size=BATCH_SIZE)
	model.save('bull_bear_model.model')
	model.save_weights("bull_bear_weight.hdf5", overwrite=True)
	#test = 'buy bull aapl stock'
	#test_model.bull_bear(test)
	#new_model = tf.keras.models.load_model('tweet_model.model')

def stock_quote(X, y, X_train, y_train, X_test, y_test, test):
	max_score = 0
	alpha = 5
	#for alp in [0.001,0.003,0.01, 0.03, 0.1, 0.3, 1, 3, 5, 8, 10]:
	#	mlpreg = MLPClassifier(solver = 'lbfgs', activation = 'tanh', alpha = alp, hidden_layer_sizes = [40,40], random_state = 0)
	#	acc_scores = cross_val_score(mlpreg,X,y,cv = 5)
	#	acc_scores = np.mean(acc_scores)
	#	if  acc_scores > max_score:
	#		alpha = alp
	#		max_score = acc_scores
	#print("opt_reg: ", alpha)
	#print("max score: ", max_score)

	mlpreg = MLPClassifier(solver = 'lbfgs', activation = 'tanh', alpha = alpha, hidden_layer_sizes = [40,40], random_state = 0)
	mlpreg.fit(X_train, y_train)
	print("*******************Evaluation*********************")
	acc_score = cross_val_score(mlpreg,X,y,cv = 5)
	acc_score = np.mean(acc_score)
	testset_prediction = mlpreg.predict(X_test)
	testset_prediction = mlpreg.predict(X_test)
	train_prediction = mlpreg.predict(X_train)
	print("Validation accuracy: ", acc_score)
	print("training set accuracy: ", accuracy_score(y_train, train_prediction))
	print("test set accuracy: ", accuracy_score(y_test, testset_prediction))
	print("Score Matrics")
	print(classification_report(y_test, testset_prediction))
	with open('candle_analysis_model.pkl', 'wb') as f:
		pickle.dump(mlpreg, f, pickle.HIGHEST_PROTOCOL)

#r_nr()
#bull_bear()

