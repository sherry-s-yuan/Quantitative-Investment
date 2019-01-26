import pandas as pd
# load
tweets = pd.read_csv('relavent_tweets.csv', header = None)
# drop NANs
tweets = tweets.dropna(how = 'any')
# extract text only
tweets_text = tweets.iloc[:, 3]
# extract likes and followers
tweets_state = tweets.iloc[:, 1:3]
# extract labels [0,1]; 1 = irrelavent, 1 = relavent
tweets_target = tweets. iloc[:, -1]

