import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Analyser(object):
	"""docstring for Analyser"""
	def __init__(self, csv = 'data/test_data_pure.csv'):
		super(Analyser, self).__init__()
		self.data = pd.read_csv(csv)user_id = [[] for i in range(12)]

		self.text_data = self.data[data['Type'] == 'text']
		self.fumoji_data = self.data[data['Type'] == 'Fumoji']
		self.audio_data = self.data[data['Type'] == 'Audio']

		self.user_id = [[] for i in range(12)]
		for i in range(2,14):#每段话有哪些user做了
		    self.user_id[i-2] = list(set((self.audio_data[self.audio_data['Talk'] == i]['UserID'].values)))

		self.talk_id = [2,3,4,5,6,7,8,9,10,11,12,13]#conversation的列表

	#calculate the k values of each segment
	def get_k_value(theList):
	    a = theList[0]
	    kList = []
	    for i in range(1, len(theList)):
	        kList.append(theList[i] - a)
	        a = theList[i]
	    return kList	


		