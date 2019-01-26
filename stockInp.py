import quandl
import datetime
import pandas as pd
import numpy as np
import math
#lastUpdate = None
#with open('date.txt') as f:
#	lastUpdate = f.readlines()
#start = lastUpdate
#end = datetime.date.today()
def finData(stock_type, collapse):
	quandl.ApiConfig.api_key = "vzWJDM8EgbfHpgvR5c9_"
	data = quandl.get(stock_type, collapse = collapse, returns = "pandas")
	#print(data)
	period = 1
	process(data, period)

def ratio_return(data_close, i):
	stock_return = data_close[i]/data_close[0]
	return stock_return

# if i < m - 1
def ratio_growth(data_close, i):
	return (data_close[i+1] - data_close[i]) / data_close[i]
# if i > 0
def ratio_increase(data_close, i):
	return (data_close[i] - data_close[i-1]) / data_close[i]
#if i > 0
def ratio_change(data_close, i):
	return math.log(data_close[i]) - math.log(data_close[i-1])

def moving_average(data_close, i, m):
	movingAverage = [np.nan for _ in range(12)]
	for j in range(1, 13):
		if i >= j * 5:
			movingAverage[j-1] = data_close.iloc[i] - np.mean(data_close.iloc[i-(j*5):i+1])
	return movingAverage

#if i < m - period
def labels(data_close, i, period):
	ave_change = sum([(data_close.iloc[i+j]-data_close.iloc[i+j-1]) for j in range(1,period+1)]) / period
	period_change = data_close.iloc[i+period] - data_close.iloc[i] 
	overal = (ave_change + period_change)/2
	#print(overal)
	#label = 3
	threshold = 0.02
	if abs(overal) <= threshold:
		return 2
	elif overal > threshold:
		return 1
	elif overal < -threshold:
		return 3
	#return label

def process(data, period):
	m, n = data.shape
	bin = [0]*3
	increase = pd.DataFrame(np.nan,  index = data.index.values, columns = ["Increase"])
	change = pd.DataFrame(np.nan,  index=data.index.values, columns = ["Change"])
	movAve = pd.DataFrame(np.nan,  index=data.index.values, columns = [i*5 for i in range(1,13)])
	label = pd.DataFrame(np.nan,  index=data.index.values, columns = ["Label"])
	data_close = data.iloc[:,10]
	for i in range(0, m):
		if i > 0:
			increase.iloc[i,0] = ratio_increase(data_close, i)
			change.iloc[i,0] = ratio_change(data_close, i)
		movAve.iloc[i,:] = moving_average(data_close, i, m)
		if i < m - period:
			bin[labels(data_close, i, period)-1] += 1
			label.iloc[i,0] = labels(data_close, i, period)
	frames = [data.iloc[:, 11], increase, change, movAve, label] 
	preprocess_data = pd.concat(frames, axis=1)
	print("bin",bin)
	with open('stockData.csv','w') as f:
			preprocess_data.to_csv(f) #header = False, index = False


#data = finData("EOD/AAPL","daily")

