import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser


ma = MimiAnalyser('data/test_data_pure.csv')
THE_TALK = 12

dfAudioV = ma.get_V_FrameByTalk(THE_TALK, 'audio')
dfAudioA = ma.get_A_FrameByTalk(THE_TALK, 'audio')

averageV = dfAudioV.apply(np.mean, axis = 0)
averageA = dfAudioA.apply(np.mean, axis = 0)

quadrantV = ma.getQuadrant(dfAudioV)
quadrantA = ma.getQuadrant(dfAudioA)

averageQV = quadrantV.apply(np.mean, axis = 0)
averageQA = quadrantA.apply(np.mean, axis = 0)

correctionQV = []
correctionQA = []

for index, r in dfAudioV.iterrows():
    correctionQV.append(ma.quadrantCorrection(averageQV, r))
for index, r in dfAudioA.iterrows():
    correctionQA.append(ma.quadrantCorrection(averageQA, r))
    
quadrantCorrectionV = pd.Series(correctionQV, index = ma.user_id[THE_TALK-2]).sort_values()
quadrantCorrectionA = pd.Series(correctionQA, index = ma.user_id[THE_TALK-2]).sort_values()

# check the k values

dfK_AudioV = ma.get_k_value(dfAudioV)
dfK_AudioA = ma.get_k_value(dfAudioA)
dfK_AudioV = ma.getQuadrant(dfK_AudioV)
dfK_AudioA = ma.getQuadrant(dfK_AudioA)

mean_k_v = dfK_AudioV.apply(np.mean, axis = 0)
mean_k_a = dfK_AudioA.apply(np.mean, axis = 0)

correctionQV_K = []
correctionQA_K = []

for index, r in dfK_AudioV.iterrows():
    correctionQV_K.append(ma.quadrantCorrection(mean_k_v, r))

for index, r in dfK_AudioA.iterrows():
    correctionQA_K.append(ma.quadrantCorrection(mean_k_a, r))

correctionQV_K = pd.Series(correctionQV_K, index = ma.user_id[THE_TALK-2]).sort_values()
correctionQA_K = pd.Series(correctionQA_K, index = ma.user_id[THE_TALK-2]).sort_values()
