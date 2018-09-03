import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser

ma = MimiAnalyser('data/test_data_filtered.csv')

def errorCurve(dAudio, dText, title):
	error = pd.Series()
	count = pd.Series()

	for i, dataOfTalk in enumerate(dAudio):
		for j, dataOfUser in enumerate(dataOfTalk):
			for k, sentenceData in enumerate(dataOfUser):
				t = dText[i][j][k]
				if error.get(sentenceData) == None:
					count.at[sentenceData] = 1
					error.at[sentenceData] = np.abs(sentenceData - t)
				else:
					count.at[sentenceData] += 1
					error.at[sentenceData] += np.abs(sentenceData - t)

	error = error.div(count).sort_index()

	print(error, count.sort_index())
	ma.plotSeries(error, title)

def errorCurveSelected(vAudio, vText, aAudio, aText, title):
	error = pd.Series()
	count = pd.Series()
	for i, dataOfTalk in enumerate(aAudio):
		for j, dataOfUser in enumerate(dataOfTalk):
			for k, sentenceData in enumerate(dataOfUser):
				if vAudio[i][j][k] < 0:
					t = aText[i][j][k]
					if error.get(sentenceData) == None:
						count.at[sentenceData] = 1
						error.at[sentenceData] = np.abs(sentenceData - t)
					else:
						count.at[sentenceData] += 1
						error.at[sentenceData] += np.abs(sentenceData - t)
	error = error.div(count).sort_index()
	count = count.sort_index()

	error1 = pd.Series()
	count1 = pd.Series()
	for i, dataOfTalk in enumerate(aAudio):
		for j, dataOfUser in enumerate(dataOfTalk):
			for k, sentenceData in enumerate(dataOfUser):
				if vAudio[i][j][k] > 0:
					t = aText[i][j][k]
					if error1.get(sentenceData) == None:
						count1.at[sentenceData] = 1
						error1.at[sentenceData] = np.abs(sentenceData - t)
					else:
						count1.at[sentenceData] += 1
						error1.at[sentenceData] += np.abs(sentenceData - t)
	error1 = error1.div(count1).sort_index()
	count1 = count1.sort_index()

	# print(error, count)
	sDict = {'error: Valence < 0': error,  'error: Valence > 0': error1}
	ma.plotDict(sDict, title)
	sDict = {'count: Valence < 0': count, 'count: Valence > 0': count1}
	ma.plotDict(sDict, title)	

# errorCurve(ma.vAudio, ma.vText, 'Error Of Valence')
# errorCurve(ma.aAudio, ma.aText, 'Error Of Arousal')

errorCurveSelected(ma.vAudio, ma.vText, ma.aAudio, ma.aText, 'Arousal')
