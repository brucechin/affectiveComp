import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]

data = pd.read_csv('data/test_data_pure.csv')


text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

fumoji_valence_error = [{} for i in range(12)]
text_valence_error = [{} for j in range(12)]

cols = ['UserID','Arousal']

# def array2Dic(array):
#     dic = {}
#     for i in array:
#         dic[i[0]] = i[1]
#     return dic
#
# def cal_error_abs(a,b):
#     result = 0
#     if(len(a) == len(b) and len(a) > 0):
#         for (key,item) in a.items():
#             result += np.abs(item - b[key])
#         return float(result / len(a))
#     else:
#         return 0

# 以第10段对话为例，画出一段话中V A各自升降趋势图

user_id = [[] for i in range(12)]

for i in range(2,14):#每段话有哪些user做了
    user_id[i-2] = list(set((audio_data[audio_data['Talk'] == i]['UserID'].values)))

talk_id = [2,3,4,5,6,7,8,9,10,11,12,13]#conversation的列表

def generate_2D_array(length):
    return [[] for i in range(length)]

def plot_figure(array,name,type,index):
    plt.figure()
    plt.title('conversation {} {} {} trace'.format(index,name,type))
    for i in range(len(array)):
        plt.plot(array[i],label = 'userid {}'.format(user_id[index][i]))
    plt.legend()
    plt.show()


valence_audio_all = []
arousal_audio_all = []

for talk in talk_id:
    count = 0
    valence_audio = generate_2D_array(len(user_id[talk-2]))
    arousal_audio = generate_2D_array(len(user_id[talk-2]))
    for i in user_id[talk - 2]:
        valence_audio[count] = audio_data[audio_data['Talk'] == talk][audio_data['UserID'] == i]['Valence'].values
        arousal_audio[count] = audio_data[audio_data['Talk'] == talk][audio_data['UserID'] == i]['Arousal'].values
        count += 1
    valence_audio_all.append(valence_audio)
    arousal_audio_all.append(arousal_audio)

for i in range(12):
    plot_figure(valence_audio_all[i],'audio','valence',i)
    plot_figure(arousal_audio_all[i],'audio','arousal',i)