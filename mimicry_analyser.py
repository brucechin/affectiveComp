import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MimiAnalyser(object):
	"""docstring for MimiAnalyser"""
	def __init__(self, csv = 'data/test_data_pure.csv'):
		super(MimiAnalyser, self).__init__()
		self.data = pd.read_csv(csv)user_id = [[] for i in range(12)]

		audio_data = self.data[self.data['Type'] == 'Audio']

		self.user_id = [[] for i in range(12)]
		for i in range(2,14):#每段话有哪些user做了
		    self.user_id[i-2] = list(set((audio_data[audio_data['Talk'] == i]['UserID'].values)))

		self.talk_id = [2,3,4,5,6,7,8,9,10,11,12,13]#conversation的列表

	def get_V_DataBy(self, UserID, Talk, Type):
		return pd.DataFrame(self.data[self.data['UserID']==UserID][self.data['Talk']==Talk][self.data['Type']==Type]['Valence'].values)
	def get_A_DataBy(self, UserID, Talk, Type)
		return pd.DataFrame(self.data[self.data['UserID']==UserID][self.data['Talk']==Talk][self.data['Type']==Type]['Arousal'].values)

	def get_V_FrameByTalk(self, Talk, Type):
		return pd.DataFrame(self.data[self.data['Talk']==Talk][self.data['Type']==Type]['Valence'].values)
	def get_A_FrameByTalk(self, Talk, Type):
		return pd.DataFrame(self.data[self.data['Talk']==Talk][self.data['Type']==Type]['Arousal'].values)

	def userIDsOfTalk(self, Talk):
		return self.user_id[Talk - 2]
	
	def getQuadrant(self, df):
	    quadrant = np.zeros(df.shape)
	    for index, row_i in df.iterrows():
	        row_i = pd.Series(row_i)
	        for index2, item in row_i.iteritems():
	            if item < 0:
	                quadrant[index][index2] = -1
	            elif item > 0:
	                quadrant[index][index2] = +1
	    quadrant = pd.DataFrame(quadrant)
	    return quadrant

	#calculate the k values of each segment
	def get_k_value(df):
	    frameK = np.zeros((df.shape[0], df.shape[1]-1))
	    for index, row in df.iterrows():
	        a = row[0]
	        for index_, item in row.iteritems():
	            if index_ > 0:
	                frameK[index][index_ - 1] = item - a
	                a = item
	    return pd.DataFrame(frameK)  

	def plotTalk(self, Talk, Type):
	    plt.figure(figsize = (28.8, 16.39))
	    plt.title('conversation {} {} {}'.format(Talk, 'valence', Type))
	    array = self.get_V_FrameByTalk(Talk, Type)
	    for i in range(len(array)):
	        plt.plot(array[i],label = 'userid {}'.format(self.user_id[Talk][i]))
	    array = pd.DataFrame(array)
	    plt.plot(array.apply(np.mean, axis = 0), label = 'average')
	    plt.legend()
	    # plt.show()
	    plt.savefig('c{}{}{}'.format(talk_id[index],name,type))
	  
	    plt.figure(figsize = (28.8, 16.39))
	    plt.title('conversation {} {} {}'.format(Talk, 'arousal', Type))
	    array = self.get_A_FrameByTalk(Talk, Type)
	    for i in range(len(array)):
	        plt.plot(array[i],label = 'userid {}'.format(self.user_id[Talk][i]))
	    array = pd.DataFrame(array)
	    plt.plot(array.apply(np.mean, axis = 0), label = 'average')
	    plt.legend()
	    # plt.show()
	    plt.savefig('c{}{}{}'.format(talk_id[index],name,type))	    



		