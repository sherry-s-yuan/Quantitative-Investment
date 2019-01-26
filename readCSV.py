import pandas as pd
import numpy as np

def readCSV():
	df = pd.read_csv('stockData.csv')
	return df.iloc[:,1:]
