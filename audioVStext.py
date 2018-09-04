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
	ma = MimiAnalyser('data/test_data_extremelyPure.csv')

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

	data = {'when Arousal < 0': errorArray[0], 'when Arousal > 0': errorArray[1]}
	ma.plotDict(data, 'error of Valence')

	data = {'when Valence < 0': errorArray[2], 'when Valence > 0': errorArray[3]}
	ma.plotDict(data, 'error of Arousal')

def errorCurvePotinFiveByAnnotation(talkSeries):
	ma = MimiAnalyser('data/test_data_extremelyPure.csv')

	errorV1 = pd.Series()
	countV1 = pd.Series()

	errorA1 = pd.Series()
	countA1 = pd.Series()


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
			eV = errorV1
			cV = countV1
			if eV.get(d) == None:
				cV.at[d] = 1
				eV.at[d] = np.abs(d - pointFive(aveTextV[i]))
			else:
				cV.at[d] += 1
				eV.at[d] += np.abs(d - pointFive(aveTextV[i]))

		for i in sentencesInTalk:
			d = pointFive(aveAudioA[i])
			eA = errorA1
			cA = countA1
			if eA.get(d) == None:
				cA.at[d] = 1
				eA.at[d] = np.abs(d - pointFive(aveTextA[i]))
			else:
				cA.at[d] += 1
				eA.at[d] += np.abs(d - pointFive(aveTextA[i]))

	eV = eV.div(cV).sort_index()
	cV = cV.sort_index()
	eA = eA.div(cA).sort_index()
	cA = cA.sort_index()

	errorArray = [eV, eA]
	countArray = [cV, cA]

	for index, countSeries in enumerate(countArray):
		for label, count in countSeries.iteritems():
			if count < 1:
				countArray[index] = countArray[index].drop(label)
				errorArray[index] = errorArray[index].drop(label)

	return [errorArray[0], errorArray[1], countArray[0], countArray[1]]
# end of errorCurvePotinFiveByAnnotation

def plotGroup(group, groupCount, title):
	plt.figure(figsize=(16, 9), dpi=80)
	plt.title(title)
	barWidth = 0.2/len(group)
	for index2, item in enumerate(groupCount):
		plt.bar(groupCount[item].index + barWidth*index2, groupCount[item].div(100).values, barWidth, alpha = 0.6,label = item+':Count/100')
	for index, item in enumerate(group):
		plt.plot(group[item], label = item + ':Error')
	
	plt.legend()
	plt.show()
	
	# plt.figure(figsize=(8, 6), dpi=80)
	# plt.title(title+' Arousal')
	# plt.plot(group1[1], label = groupLabel1 + 'Arousal')
	# plt.plot(group2[1], label = groupLabel2 + 'Arousal')
	# barWidth = 0.1

	# plt.bar(male[3].index - barWidth*0.5, male[3].div(100).values, barWidth, label = groupLabel1+'Count/100')
	# plt.bar(female[3].index + barWidth*0.5, female[3].div(100).values, barWidth, label = groupLabel2+'Count/100')
	# plt.legend()
	# plt.show()		

ma = MimiAnalyser('data/test_data_filtered.csv')
a = Annotation()

errorCurvePotinFive()


# series_maleSpeakers = a.getTalkSentenceByAnnotation('说话人性别','男')
# series_femaleSpeakers = a.getTalkSentenceByAnnotation('说话人性别','女')
# male = errorCurvePotinFiveByAnnotation(series_maleSpeakers)
# female = errorCurvePotinFiveByAnnotation(series_femaleSpeakers)

# genderGroupV = {'male':male[0], 'female':female[0]}
# genderGroupVCount = {'male':male[2], 'female':female[2]}
# plotGroup(genderGroupV, genderGroupVCount,'genderGroupValence')

# genderGroupA = {'male':male[1], 'female':female[1]}
# genderGroupACount = {'male':male[3], 'female':female[3]}
# plotGroup(genderGroupA, genderGroupACount, 'genderGroupArousal')

# errorCurve(ma.vAudio, ma.vText, 'Error Of Valence')
# errorCurve(ma.aAudio, ma.aText, 'Error Of Arousal')

# errorCurveSelected(ma.vAudio, ma.vText, ma.aAudio, ma.aText, 'Arousal')

# series_withMood = a.getTalkSentenceByAnnotation('文本有无语气词','有')
# series_withoutMood = a.getTalkSentenceByAnnotation('文本有无语气词','无')
# withMood = errorCurvePotinFiveByAnnotation(series_withMood)
# withoutMood = errorCurvePotinFiveByAnnotation(series_withoutMood)

# moodGroupV = {'withMood':withMood[0], 'withoutMood':withoutMood[0]}
# moodGroupVCount = {'withMood':withMood[2], 'withoutMood':withoutMood[2]}
# plotGroup(moodGroupV, moodGroupVCount,'moodGroupValence')
# moodGroupA = {'withMood':withMood[1], 'withoutMood':withoutMood[1]}
# moodGroupACount = {'withMood':withMood[3], 'withoutMood':withoutMood[3]}
# plotGroup(moodGroupA, moodGroupACount,'moodGroupArousal')

# series_positive = a.getTalkSentenceByAnnotation('句式','肯定句')
# series_rehtorQuestion = a.getTalkSentenceByAnnotation('句式','反问句')
# series_question = a.getTalkSentenceByAnnotation('句式','疑问句')
# series_negative = a.getTalkSentenceByAnnotation('句式','否定句')
# series_imperative = a.getTalkSentenceByAnnotation('句式','祈使句')

# positive = errorCurvePotinFiveByAnnotation(series_positive)
# rehtorQuestion = errorCurvePotinFiveByAnnotation(series_rehtorQuestion)
# question = errorCurvePotinFiveByAnnotation(series_question)
# negative = errorCurvePotinFiveByAnnotation(series_negative)
# imperative = errorCurvePotinFiveByAnnotation(series_imperative)

# sentencePatternGroupV = {'positive':positive[0], 'rehtorQuestion':rehtorQuestion[0], 'question': question[0], 'negative':negative[0], 'imperative':imperative[0]}
# sentencePatternVCount =  {'positive':positive[2], 'rehtorQuestion':rehtorQuestion[2], 'question': question[2], 'negative':negative[2], 'imperative':imperative[2]}
# plotGroup(sentencePatternGroupV, sentencePatternVCount,'sentencePatternGroupValence')
# sentencePatternGroupA = {'positive':positive[1], 'rehtorQuestion':rehtorQuestion[1], 'question': question[1], 'negative':negative[1], 'imperative':imperative[1]}
# sentencePatternGroupACount = {'positive':positive[3], 'rehtorQuestion':rehtorQuestion[3], 'question': question[3], 'negative':negative[3], 'imperative':imperative[3]}
# plotGroup(sentencePatternGroupA, sentencePatternGroupACount,'sentencePatternGroupArousal')