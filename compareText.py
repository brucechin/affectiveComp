import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser

ma = MimiAnalyser('data/test_data_filtered.csv')
THE_TALK = 5

dfAudioV = ma.get_V_FrameByTalk(THE_TALK, 'Audio')
dfAudioA = ma.get_A_FrameByTalk(THE_TALK, 'Audio')

aveAudioV = dfAudioV.apply(np.mean, axis = 0)
aveAudioA = dfAudioA.apply(np.mean, axis = 0)

dfTextV = ma.get_V_FrameByTalk(THE_TALK, 'text')
dfTextA = ma.get_A_FrameByTalk(THE_TALK, 'text')

aveTextV = dfTextV.apply(np.mean, axis = 0)
aveTextA = dfTextA.apply(np.mean, axis = 0)

dfFumojiV = ma.get_V_FrameByTalk(THE_TALK, 'Fumoji')
dfFumojiA = ma.get_A_FrameByTalk(THE_TALK, 'Fumoji')

aveFumojiV = dfFumojiV.apply(np.mean, axis = 0)
aveFumojiA = dfFumojiA.apply(np.mean, axis = 0)

data = {"aveAudioV" : aveAudioV.values, "aveFumojiV" : aveFumojiV.values, "aveTextV" : aveTextV.values}


print("fumoji error:", ma.getErrorOfSeries(aveAudioV, aveFumojiV),"text error:", ma.getErrorOfSeries(aveAudioV, aveTextV))

print("fumoji winning rate:", ma.getWinningRate(text = aveTextV, fumo = aveFumojiV, audi = aveAudioV))
ma.plotDict(data)
