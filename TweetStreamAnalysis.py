# tweetws streaming
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, Cursor
import csv
import twitter_credential
import pandas as pd
import pickle
import numpy as np
import random
from time import sleep
# customize class
#import test_model
import predict


class StdOutListener(StreamListener):
	# streaming tweets and extract info to save to tweets.csv
	def on_data(self, data):
		#print(data)
		text = ""
		# extract full text if available, else extract partial text
		if len(data.split('"full_text":"')) > 1:
			text = data.split('"full_text":"')[1].split('",')[0]
		else:
			text = data.split(',"text":"')[1].split('",')[0]
		# bool apend, true for ralevent, false for non-ralevent
		relavent = predict.relavent(text)
		
		# extract date created
		date = data.split('"created_at":"')[1].split('",')[0] # :" ",
		# extract num_followers
		num_follower = data.split('"followers_count":')[1].split(',')[0] #: ,
		# extract num_likes
		likes = data.split('"favourites_count":')[1].split(',')[0]
		# print information
		print("date", date)
		print("follow", num_follower)
		print("likes", likes)
		# save tweets to tweets.csv and relavent_tweet.csv if relavent
		if relavent == 1:
			bull_bear_score = predict.bull_bear(text)
			raw_tweet = pd.DataFrame([date, num_follower, likes, text, 1])
			relavent_tweet = pd.DataFrame([date, num_follower, likes, text, bull_bear_score])
			with open("tweets.csv", 'a') as f:
				raw_tweet.T.to_csv(f, header = False, index = False)
			with open("relavent_tweets.csv", 'a') as f:
				relavent_tweet.T.to_csv(f, header = False, index = False)
		else:
			if random.randint(0,6) == 1:
				raw_tweet = pd.DataFrame([date, num_follower, likes, text, 0])
				with open("tweets.csv", 'a') as f:
					raw_tweet.T.to_csv(f, header = False, index = False)
		return True

	def on_error(self, status):
		print(status)

def tweets_streaming():
	try:
		Listener = StdOutListener()
		# authentication
		auth = OAuthHandler(twitter_credential.consumer_key, twitter_credential.consumer_secret)
		auth.set_access_token(twitter_credential.access_token, twitter_credential.access_secret)
		#Streaming
		stream = Stream(auth, Listener)
		# track keywords
		stream.filter(track = twitter_credential.track)
	except KeyboardInterrupt:
		print('')
		print('Program interupted...')
		#unknown error
	except:
		print("Wait 15 minutes...")
		sleep(30)


def news_streaming(paragraph, date):
	for text in paragraph.split("."):
		relavent = predict.relavent(text)
		if relavent:
			bull_bear_score = predict.bull_bear(text)
			raw_tweet = pd.DataFrame([date, 5150, 5150, text, 1])
			relavent_tweet = pd.DataFrame([date, 5150, 5150, text, bull_bear_score])
			with open("tweets.csv", 'a') as f:
				raw_tweet.T.to_csv(f, header = False, index = False)
			with open("relavent_tweets.csv", 'a') as f:
				relavent_tweet.T.to_csv(f, header = False, index = False)
		else:
			if random.randint(0,6) == 1:
				raw_tweet = pd.DataFrame([date, 5150, 5150, text, 0])
				with open("tweets.csv", 'a') as f:
					raw_tweet.T.to_csv(f, header = False, index = False)


#if __name__ == "__main__":
#	Listener = StdOutListener()
#	# authentication
#	auth = OAuthHandler(twitter_credential.consumer_key, twitter_credential.consumer_secret)
#	auth.set_access_token(twitter_credential.access_token, twitter_credential.access_secret)
#	#Streaming
#	stream = Stream(auth, Listener)
#	# track keywords
#	stream.filter(track = ["AAPL", "apple stock", "AAPL stock", "apple stock market", "$AAPL", "stocktwits AAPL", "nasdaq aapl"])
