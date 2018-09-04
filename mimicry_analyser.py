import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MimiAnalyser(object):
	"""docstring for MimiAnalyser"""
	def __init__(self, csv = 'data/test_data_pure.csv'):
		super(MimiAnalyser, self).__init__()
		self.data = pd.read_csv(csv)
		audio_data = self.data[self.data['Type'] == 'Audio']
		fumoji_data = self.data[self.data['Type'] == 'Fumoji']
		text_data = self.data[self.data['Type'] == 'text']
		self.usersOfTalk = [[] for i in range(12)]
		for i in range(2,14):#每段话有哪些user做了
		    self.usersOfTalk[i-2] = list(set((audio_data[audio_data['Talk'] == i]['UserID'].values)))

		self.talk_id = [2,3,4,5,6,7,8,9,10,11,12,13]#conversation的列表
		# [Talk-2][UserID][Sentence]
		self.vAudio = []
		self.aAudio = []
		self.vFumoji = []
		self.aFumoji = []		
		self.vText = []
		self.aText = []
		for talk in self.talk_id:
			count = 0
			valence_audio = self.generate_2D_array(len(self.usersOfTalk[talk-2]))
			arousal_audio = self.generate_2D_array(len(self.usersOfTalk[talk-2]))
			valence_fumoji = self.generate_2D_array(len(self.usersOfTalk[talk-2]))
			arousal_fumoji = self.generate_2D_array(len(self.usersOfTalk[talk-2]))
			valence_text = self.generate_2D_array(len(self.usersOfTalk[talk-2]))
			arousal_text = self.generate_2D_array(len(self.usersOfTalk[talk-2]))		    		    
			for i in self.usersOfTalk[talk - 2]:
				d = audio_data.query("(UserID == {}) and (Talk == {})".format(i, talk))
				valence_audio[count] = d['Valence'].values
				arousal_audio[count] = d['Arousal'].values
				d = fumoji_data.query("(UserID == {}) and (Talk == {})".format(i, talk))
				valence_fumoji[count] = d['Valence'].values
				arousal_fumoji[count] = d['Arousal'].values
				d = text_data.query("(UserID == {}) and (Talk == {})".format(i, talk))
				valence_text[count] = d['Valence'].values
				arousal_text[count] = d['Arousal'].values
				count += 1
			self.vAudio.append(valence_audio)
			self.aAudio.append(arousal_audio)
			self.vFumoji.append(valence_fumoji)
			self.aFumoji.append(arousal_fumoji)
			self.vText.append(valence_text)
			self.aText.append(arousal_text)
		# print(self.vAudio)

	def generate_2D_array(self, length):
	    return [[] for i in range(length)]

	def get_V_DataBy(self, UserID, Talk, Type):
		if Type == 'text':
			return pd.Series(self.vText[Talk-2][UserID])
		elif Type == 'Audio':
			return pd.Series(self.vAudio[Talk-2][UserID])
		elif Type == 'Fumoji':
			return pd.Series(self.vFumoji[Talk-2][UserID])			

	def get_A_DataBy(self, UserID, Talk, Type):
		if Type == 'text':
			return pd.Series(self.aText[Talk-2][UserID])
		elif Type == 'Audio':
			return pd.Series(self.aAudio[Talk-2][UserID])
		elif Type == 'Fumoji':
			return pd.Series(self.aFumoji[Talk-2][UserID])	

	def get_V_FrameByTalk(self, Talk, Type):
		if Type == 'text':
			return pd.DataFrame(self.vText[Talk-2], self.usersOfTalk[Talk-2])
		elif Type == 'Audio':
			return pd.DataFrame(self.vAudio[Talk-2], self.usersOfTalk[Talk-2])
		elif Type == 'Fumoji':
			return pd.DataFrame(self.vFumoji[Talk-2], self.usersOfTalk[Talk-2])

	def get_A_FrameByTalk(self, Talk, Type):
		if Type == 'text':
			return pd.DataFrame(self.aText[Talk-2], self.usersOfTalk[Talk-2])
		elif Type == 'Audio':
			return pd.DataFrame(self.aAudio[Talk-2], self.usersOfTalk[Talk-2])
		elif Type == 'Fumoji':
			return pd.DataFrame(self.aFumoji[Talk-2], self.usersOfTalk[Talk-2])
	
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

	def quadrantCorrection(self, norm_list, test_list):
	    correct_count = 0
	    for index, item in norm_list.iteritems():
	        if (item * test_list[index] > 0) or (item == test_list[index]):
	           correct_count += 1
	    return correct_count/len(norm_list)	    

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
	        plt.plot(array[i],label = 'userid {}'.format(self.usersOfTalk[Talk-2][i]))
	    array = pd.DataFrame(array)
	    plt.plot(array.apply(np.mean, axis = 0), label = 'average')
	    plt.legend()
	    # plt.show()
	    plt.savefig('c{}{}{}'.format(talk_id[index],name,type))
	  
	    plt.figure(figsize = (28.8, 16.39))
	    plt.title('conversation {} {} {}'.format(Talk, 'arousal', Type))
	    array = self.get_A_FrameByTalk(Talk, Type)
	    for i in range(len(array)):
	        plt.plot(array[i],label = 'userid {}'.format(self.usersOfTalk[Talk-2][i]))
	    array = pd.DataFrame(array)
	    plt.plot(array.apply(np.mean, axis = 0), label = 'average')
	    plt.legend()
	    # plt.show()
	    plt.savefig('c{}{}{}'.format(talk_id[index],name,type))	

	def plotDict(self, dictionary, title):
	    plt.figure(figsize = (14.4, 8))
	    plt.title(title)
	    for key, item in dictionary.items():
	        plt.plot(item, label = key)
	    plt.legend()
	    plt.show()

	def plotSeries(self, s, title):
		plt.figure(figsize = (14.4, 8))
		plt.title(title)
		plt.plot(s)
		plt.legend()
		plt.show()

	def getErrorOfSeries(self, s1, s2):
		error = 0
		count = 0
		for index, item in s1.iteritems():
			error += np.abs(s2[index] - item)
			count += 1
		return error/count

	def getWinningRate(self, text, fumo, audi):
		bingo = 0
		count = 0
		for index, item in audi.iteritems():
			if np.abs(fumo[index] - audi[index]) < np.abs(text[index] - audi[index]):
				bingo +=1
			count += 1
		return bingo/count		
	  


		