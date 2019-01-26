#Self Written
import readCSV
import predict
import stockInp
import TweetStreamAnalysis
import trainModel
#import readJSON
#import KNN
#import SVM
#import decTree

#Import Library
import pandas as pd
import numpy as np
import math
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
import pickle
import dictionary
import spider
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.model_selection import cross_val_score, GridSearchCV

# read csv file
# https://www.msn.com/en-ca/money/video/should-canada-ban-huawei/vi-BBRvND7
# get most recent stock data
try:
	if_read_tweet = int(input("Update Tweets? (1, 0): "))
	if_spider = int(input("Spider more news? (1, 0): "))
	if_read_allow = input("Update stock data? (1, 0): ")
	if_train_candle = int(input("Train Candle? (1, 0): "))
	if_train_relavence = int(input("Train relavence? (1, 0): "))
	if_train_bull_bear = int(input("Train bull-bear? (1, 0): "))
except:
	print("Invalid input, All canceled")
	if_read_tweet = 0
	if_spider = 0
	if_read_allow = 0
	if_train_candle = 0
	if_train_relavence = 0
	if_train_bull_bear = 0

#train test split

#feature normalization
#scaler = MinMaxScaler()
#scaler.fit(X_train)
#X_train_scaled = scaler.transform(X_train)
#X_test_scaled = scaler.transform(X_test)

#print("///////////////////////KNN////////////////////////")
#KNN.KNN(X, y, X_train, y_train, X_test, y_test, test)
#print("///////////////////////SVM////////////////////////")
#SVM.SVM(X, y, X_train, y_train, X_test, y_test, test)
#print("//////////////////////DecTree/////////////////////")
#decTree.decTree(X, y, X_train, y_train, X_test, y_test, test)
#print("//////////////////////NeuralNet/////////////////////")

#def train():
#	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2)
#	mlpreg = trainModel.stock_quote(X, y, X_train, y_train, X_test, y_test, test)
#	with open('candle_analysis_model.pkl', 'wb') as f:
#		pickle.dump(mlpreg, f, pickle.HIGHEST_PROTOCOL)

# train candle data, relavence data, bullish-bearish data


if int(if_read_allow):
	print("READING STOCK DATA...")
	stockInp.finData("EOD/AAPL","daily")

print("EXTRACTING DATA...")
X = readCSV.readCSV().iloc[1:,1:]
# drop data with NAN value
test = X.iloc[-7:, :-1]
X = X.dropna(how = 'any')
# reorganize data X and y
y = X.iloc[:, -1]
X = X.iloc[:, 0:-1]

# shape
m, n = X.shape


try:
	if int(if_spider):
		starturl = input('Enter web url or enter to retrieve default url')
		print("SPIDERING...")
		spider.spider(starturl)
	if int(if_read_tweet):
		print("READING TWEETWS...")
		TweetStreamAnalysis.tweets_streaming()
except KeyboardInterrupt:
	print("Interrupted by user...")

if int(if_train_candle):
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 2)
	trainModel.stock_quote(X, y, X_train, y_train, X_test, y_test, test)
if int(if_train_relavence):
	print("TRAINING RELAVENCE...")
	trainModel.r_nr()
if int(if_train_bull_bear):
	print("TRAINING BULL-BEAR...")
	trainModel.bull_bear()

print("SCORING for 7 days (1 = bullish, 2 = hold, 3 = bearish)...")
#print candle score
candle_score = predict.stock_quote(test)
# print tweet score
print("tweet score: ", predict.tweet_score(20))


