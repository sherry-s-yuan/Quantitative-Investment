# This class load tweets from tweets.csv #
import pandas as pd
# load
tweets = pd.read_csv('tweets.csv', header = None)
# drop NANs
tweets = tweets.dropna(how = 'any')
# drop duplicates
tweets.drop_duplicates(subset=[tweets.columns.values[3]], keep=False)
# extract text only
tweets_text = tweets.iloc[:, 3]
# extract likes and followers
tweets_state = tweets.iloc[:, 1:3]
# extract labels [0,1]; 1 = irrelavent, 1 = relavent
tweets_target = tweets. iloc[:, -1]

