import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser
from annotation_analyser import Annotation

def pointFive(f):
	i = np.around(f)
	if i > f:
		i -= 1
	decimal = f - i
	if decimal < 0.25:
		decimal = 0
	elif decimal >= 0.25 and decimal < 0.75:
		decimal = 0.5
	else:
		decimal = 1
	return i + decimal

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

	print(error, count)
	sDict = {'error: Valence < 0': error,  'error: Valence > 0': error1}
	ma.plotDict(sDict, title)
	sDict = {'count: Valence < 0': count, 'count: Valence > 0': count1}
	ma.plotDict(sDict, title)

def errorCurvePotinFive():
	ma = MimiAnalyser('data/test_data_filtered.csv')

	errorV1 = pd.Series()
	countV1 = pd.Series()

	errorV2 = pd.Series()
	countV2 = pd.Series()

	errorA1 = pd.Series()
	countA1 = pd.Series()

	errorA2 = pd.Series()
	countA2 = pd.Series()

	for talk in ma.talk_id:
		dfAudioV = ma.get_V_FrameByTalk(talk, 'Audio')
		dfAudioA = ma.get_A_FrameByTalk(talk, 'Audio')

		aveAudioV = dfAudioV.apply(np.mean, axis = 0)
		aveAudioA = dfAudioA.apply(np.mean, axis = 0)

		dfTextV = ma.get_V_FrameByTalk(talk, 'text')
		dfTextA = ma.get_A_FrameByTalk(talk, 'text')

		aveTextV = dfTextV.apply(np.mean, axis = 0)
		aveTextA = dfTextA.apply(np.mean, axis = 0)

		for i in range(aveAudioV.size):
			d = pointFive(aveAudioV[i])
			if aveAudioA[i] < 0:
				eV = errorV1
				cV = countV1
			elif aveAudioA[i] > 0:
				eV = errorV2
				cV = countV2
			if eV.get(d) == None:
				cV.at[d] = 1
				eV.at[d] = np.abs(d - pointFive(aveTextV[i]))
			else:
				cV.at[d] += 1
				eV.at[d] += np.abs(d - pointFive(aveTextV[i]))

		for i in range(aveAudioA.size):
			d = pointFive(aveAudioA[i])
			if aveAudioV[i] < 0:
				eA = errorA1
				cA = countA1
			elif aveAudioV[i] > 0:
				eA = errorA2
				cA = countA2
			if eA.get(d) == None:
				cA.at[d] = 1
				eA.at[d] = np.abs(d - pointFive(aveTextA[i]))
			else:
				cA.at[d] += 1
				eA.at[d] += np.abs(d - pointFive(aveTextA[i]))

	errorV1 = errorV1.div(countV1).sort_index()
	countV1 = countV1.sort_index()
	errorA1 = errorA1.div(countA1).sort_index()
	countA1 = countA1.sort_index()
	errorV2 = errorV2.div(countV2).sort_index()
	countV2 = countV2.sort_index()
	errorA2 = errorA2.div(countA2).sort_index()
	countA2 = countA2.sort_index()

	errorArray = [errorV1, errorV2, errorA1, errorA2]
	countArray = [countV1, countV2, countA1, countA2]

	for index, countSeries in enumerate(countArray):
		for label, count in countSeries.iteritems():
			if count < 3:
				countArray[index] = countArray[index].drop(label)
				errorArray[index] = errorArray[index].drop(label)

	print(countArray)

	data = {'when Arousal < 0': errorArray[0], 'when Arousal > 0': errorArray[1]}
	ma.plotDict(data, 'error of Valence')

	data = {'when Valence < 0': errorArray[2], 'when Valence > 0': errorArray[3]}
	ma.plotDict(data, 'error of Arousal')

def errorCurvePotinFiveByAnnotation(talkSeries):
	ma = MimiAnalyser('data/test_data_filtered.csv')

	errorV1 = pd.Series()
	countV1 = pd.Series()

	errorV2 = pd.Series()
	countV2 = pd.Series()

	errorA1 = pd.Series()
	countA1 = pd.Series()

	errorA2 = pd.Series()
	countA2 = pd.Series()

	for talk, sentencesInTalk in talkSeries.iteritems():
		dfAudioV = ma.get_V_FrameByTalk(talk, 'Audio')
		dfAudioA = ma.get_A_FrameByTalk(talk, 'Audio')

		aveAudioV = dfAudioV.apply(np.mean, axis = 0)
		aveAudioA = dfAudioA.apply(np.mean, axis = 0)

		dfTextV = ma.get_V_FrameByTalk(talk, 'text')
		dfTextA = ma.get_A_FrameByTalk(talk, 'text')

		aveTextV = dfTextV.apply(np.mean, axis = 0)
		aveTextA = dfTextA.apply(np.mean, axis = 0)
		for i in sentencesInTalk:
			d = pointFive(aveAudioV[i])
			if aveAudioA[i] < 0:
				eV = errorV1
				cV = countV1
			elif aveAudioA[i] > 0:
				eV = errorV2
				cV = countV2
			if eV.get(d) == None:
				cV.at[d] = 1
				eV.at[d] = np.abs(d - pointFive(aveTextV[i]))
			else:
				cV.at[d] += 1
				eV.at[d] += np.abs(d - pointFive(aveTextV[i]))

		for i in range(aveAudioA.size):
			d = pointFive(aveAudioA[i])
			if aveAudioV[i] < 0:
				eA = errorA1
				cA = countA1
			elif aveAudioV[i] > 0:
				eA = errorA2
				cA = countA2
			if eA.get(d) == None:
				cA.at[d] = 1
				eA.at[d] = np.abs(d - pointFive(aveTextA[i]))
			else:
				cA.at[d] += 1
				eA.at[d] += np.abs(d - pointFive(aveTextA[i]))

	errorV1 = errorV1.div(countV1).sort_index()
	countV1 = countV1.sort_index()
	errorA1 = errorA1.div(countA1).sort_index()
	countA1 = countA1.sort_index()
	errorV2 = errorV2.div(countV2).sort_index()
	countV2 = countV2.sort_index()
	errorA2 = errorA2.div(countA2).sort_index()
	countA2 = countA2.sort_index()

	errorArray = [errorV1, errorV2, errorA1, errorA2]
	countArray = [countV1, countV2, countA1, countA2]

	for index, countSeries in enumerate(countArray):
		for label, count in countSeries.iteritems():
			if count < 3:
				countArray[index] = countArray[index].drop(label)
				errorArray[index] = errorArray[index].drop(label)

	print(countArray)

	data = {'when Arousal < 0': errorArray[0], 'when Arousal > 0': errorArray[1]}
	ma.plotDict(data, 'error of Valence FemaleSpeakers')

	data = {'when Valence < 0': errorArray[2], 'when Valence > 0': errorArray[3]}
	ma.plotDict(data, 'error of Arousal FemaleSpeakers')


ma = MimiAnalyser('data/test_data_filtered.csv')
a = Annotation()

series_maleSpeakers = a.getTalkSentenceByAnnotation('说话人性别','男')
series_femaleSpeakers = a.getTalkSentenceByAnnotation('说话人性别','女')
print(series_femaleSpeakers)
# errorCurvePotinFiveByAnnotation(series_maleSpeakers)
errorCurvePotinFiveByAnnotation(series_femaleSpeakers)

# errorCurve(ma.vAudio, ma.vText, 'Error Of Valence')
# errorCurve(ma.aAudio, ma.aText, 'Error Of Arousal')

# errorCurveSelected(ma.vAudio, ma.vText, ma.aAudio, ma.aText, 'Arousal')
