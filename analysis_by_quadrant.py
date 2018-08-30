import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]#每段话有多少句话

data = pd.read_csv('data/test_data_pure.csv')


text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']
talk_id = [2,3,4,5,7,8,9,10,11,12,13]#conversation的列表

valence_text_error = [[] for i in range(4)]#四个象限的误差分别记录
arousal_text_error  = [[] for i in range(4)]
valence_fumoji_error = [[] for i in range(4)]
arousal_fumoji_error = [[] for i in range(4)]


for talk in talk_id:
    text_valence_error_tmp = []
    text_arousal_error_tmp = []
    for sentence in range(1,talk_length[talk-2] + 1):
        audio_valence_mean = np.mean(audio_data[audio_data['Talk'] == talk][audio_data['Sentence'] == sentence][['Valence']].values)
        audio_arousal_mean = np.mean(audio_data[audio_data['Talk'] == talk][audio_data['Sentence'] == sentence][['Arousal']].values)
        text_valence_mean = np.mean(text_data[text_data['Talk'] == talk][text_data['Sentence'] == sentence]['Valence'].values)
        text_arousal_mean = np.mean(text_data[text_data['Talk'] == talk][text_data['Sentence'] == sentence]['Arousal'].values)
        fumoji_valence_mean = np.mean(fumoji_data[fumoji_data['Talk'] == talk][fumoji_data['Sentence'] == sentence]['Valence'].values)
        fumoji_arousal_mean = np.mean(fumoji_data[fumoji_data['Talk'] == talk][fumoji_data['Sentence'] == sentence]['Arousal'].values)
        loc = 0 #判断audio 情感在第几象限
        if(audio_arousal_mean > 0 and audio_valence_mean > 0):
            loc = 0
        elif(audio_valence_mean < 0 and audio_arousal_mean > 0):
            loc = 1
        elif(audio_valence_mean < 0 and audio_arousal_mean < 0):
            loc = 2
        elif(audio_valence_mean > 0 and audio_arousal_mean < 0):
            loc = 3
        valence_text_error[loc].append(np.abs(text_valence_mean - audio_valence_mean))
        arousal_text_error[loc].append(np.abs(text_arousal_mean - audio_arousal_mean))
        valence_fumoji_error[loc].append(np.abs(fumoji_valence_mean - audio_valence_mean))
        arousal_fumoji_error[loc].append(np.abs(fumoji_arousal_mean - audio_arousal_mean))

for i in range(4):
    print('Fumoji the {} quarter valence error mean {} arousal error mean {}'.format(i+1,np.mean(valence_fumoji_error[i]),np.mean(arousal_fumoji_error[i])))
    print('Text the {} quarter valence error mean {} arousal error mean {}'.format(i+1,np.mean(valence_text_error[i]),np.mean(arousal_text_error[i])))

