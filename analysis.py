import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# record / line / type / valence / arousal

# 与语音mean的差别

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]

data = pd.read_csv('data/fumoji.csv')

text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

fumoji_valence_error = []
text_valence_error = []
arousal_error = []

cols = [col for col in data.columns if col in ['Arousal']]

#print(data.groupby('Type')[cols].mean()) #查看全部数据中Audio Fumoji Text三种之间的差距



# for i in range(2,14):
#     for j in range(talk_length[i-2]+1):
#         text_valence_error.append(text_data[text_data['Talk'] == i][text_data['Sentence'] == j][cols].mean() - audio_data[audio_data['Talk'] == i][audio_data['Sentence'] == j][cols].mean())
#         fumoji_valence_error.append(fumoji_data[fumoji_data['Talk'] == i][fumoji_data['Sentence'] == j][cols].mean() - audio_data[audio_data['Talk'] == i][audio_data['Sentence'] == j][cols].mean())
#
# print(len(text_valence_error))
# plt.figure()
# plt.title('arousal error comparison')
# plt.plot(text_valence_error,label='text error')
# plt.plot(fumoji_valence_error,label = 'fumoji error')
# plt.xlabel('sentence')
# plt.legend()
# plt.show()
