import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]#每段话有多少句话

data = pd.read_csv('data/test_data_filtered.csv')


text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']
talk_id = [2,3,4,5,7,8,9,10,11,12,13]#conversation的列表

valence_text_error = [[] for i in range(4)]#四个象限的误差分别记录
arousal_text_error  = [[] for i in range(4)]
valence_fumoji_error = [[] for i in range(4)]
arousal_fumoji_error = [[] for i in range(4)]

users_of_talk = []
for i in range(2, 14):  # 每段话有哪些user做了
    users_of_talk.append(list(set((audio_data[audio_data['Talk'] == i]['UserID'].values))))


filtered_sentences_all = {}#记录下error std 在正常范围内的talk-sentence id

for talk in talk_id:
    if talk != 6:
        filtered_sentences = []
        for sentence in range(1,talk_length[talk-2] + 1):
            text_valence_error_tmp = []
            text_arousal_error_tmp = []
            fumoji_valence_error_tmp = []
            fumoji_arousal_error_tmp = []
            for user in users_of_talk[talk-2]:
                text_data_tmp = text_data[text_data['Talk'] == talk][text_data['Sentence'] == sentence][text_data['UserID'] == user]
                fumoji_data_tmp = fumoji_data[fumoji_data['Talk'] == talk][fumoji_data['Sentence'] == sentence][fumoji_data['UserID'] == user]
                audio_data_tmp = audio_data[audio_data['Talk'] == talk][audio_data['Sentence'] == sentence][audio_data['UserID'] == user]
                if(len(text_data_tmp) > 0 and len(fumoji_data_tmp) > 0 and len(audio_data_tmp) > 0):
                    text_valence_error_tmp.append(text_data_tmp['Valence'].values[0] - audio_data_tmp['Valence'].values[0])
                    text_arousal_error_tmp.append(text_data_tmp['Arousal'].values[0] - audio_data_tmp['Arousal'].values[0])
                    fumoji_valence_error_tmp.append(fumoji_data_tmp['Valence'].values[0] - audio_data_tmp['Valence'].values[0])
                    fumoji_arousal_error_tmp.append(fumoji_data_tmp['Arousal'].values[0] - audio_data_tmp['Arousal'].values[0])

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
            # print('talk {} sentence {}'.format(talk,sentence))
            # print('text valence error std{}'.format(np.std(text_valence_error_tmp)))
            # print('text arousal error std{}'.format(np.std(text_arousal_error_tmp)))
            # print('fumoji valence error std{}'.format(np.std(fumoji_valence_error_tmp)))
            # print('fumoji_arousal_error std{}'.format(np.std(fumoji_arousal_error_tmp)))

            bottleneck = 1.5
            if(np.std(text_valence_error_tmp) < bottleneck and np.std(text_arousal_error_tmp) < bottleneck):
                valence_text_error[loc].append(np.abs(text_valence_mean - audio_valence_mean))
                arousal_text_error[loc].append(np.abs(text_arousal_mean - audio_arousal_mean))
                filtered_sentences.append(sentence)
            if(np.std(fumoji_valence_error_tmp) < bottleneck and np.std(fumoji_arousal_error_tmp) < bottleneck):
                valence_fumoji_error[loc].append(np.abs(fumoji_valence_mean - audio_valence_mean))
                arousal_fumoji_error[loc].append(np.abs(fumoji_arousal_mean - audio_arousal_mean))
        filtered_sentences_all[talk] = pd.Series(filtered_sentences)

print(filtered_sentences_all)

print('when remove error std lager than {}'.format(bottleneck))

for i in range(4):
    print('Fumoji the {} quarter valence error mean {} arousal error mean {}, has {} sentences'.format(i+1,np.mean(valence_fumoji_error[i]),np.mean(arousal_fumoji_error[i]),len(valence_text_error[i])))
    print('Text the {} quarter valence error mean {} arousal error mean {}, has {} sentences'.format(i+1,np.mean(valence_text_error[i]),np.mean(arousal_text_error[i]),len(valence_text_error[i])))

