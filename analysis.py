import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]

user_id = [i for i in range(60)]
data = pd.read_csv('data/test_data_pure.csv')


text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

fumoji_valence_error = [{} for i in range(12)]
text_valence_error = [{} for j in range(12)]

cols = ['UserID','Arousal']

def array2Dic(array):
    dic = {}
    for i in array:
        dic[i[0]] = i[1]
    return dic

def cal_error_abs(a,b):
    result = 0
    if(len(a) == len(b) and len(a) > 0):
        for (key,item) in a.items():
            result += np.abs(item - b[key])
        return float(result / len(a))
    else:
        return 0

#  此段为画出每句text/fumoji 与audio的误差折线图
# for i in range(2,14):
#     for j in range(1,talk_length[i-2]+1):
#         text_dic = array2Dic(text_data[text_data['Talk'] == i][text_data['Sentence'] == j][cols].values)
#         audio_dic = array2Dic(audio_data[audio_data['Talk'] == i][audio_data['Sentence'] == j][cols].values)
#         fumoji_dic = array2Dic(fumoji_data[fumoji_data['Talk'] == i][fumoji_data['Sentence'] == j][cols].values)
#         text_error = cal_error_abs(text_dic,audio_dic)
#         fumoji_error = cal_error_abs(fumoji_dic,audio_dic)
#         text_valence_error[i-2][j] = text_error
#         fumoji_valence_error[i-2][j] = fumoji_error

# for i in range(12):
#     print('Talk {} text {} error mean : {}'.format(i+2,cols, np.abs(text_valence_error[i]).mean()))
#     print('Talk {} fumoji {} error mean : {}'.format(i+2,cols, np.abs(fumoji_valence_error[i]).mean()))
#     plt.figure()
#     plt.title('Talk {} {} error comparison'.format(i+2,cols))
#     plt.plot(np.abs(text_valence_error[i]),label='text error')
#     plt.plot(np.abs(fumoji_valence_error[i]),label = 'fumoji error')
#     plt.xlabel('sentence')
#     plt.legend()
#     plt.show()



# 以第10段对话为例，画出一段话中V A各自升降趋势图

def generate_2D_array(length):
    return [[] for i in range(length)]


def plot_figure(array,name,type):
    plt.figure()
    plt.title('{} {} trace'.format(name,type))
    for i in range(len(array)):
        plt.plot(array[i],label = 'userid {}'.format(user_id[i]))
    plt.legend()
    plt.show()

user_id_10 = [20,22,27,28,29]
talk_id = 10
valence_audio = generate_2D_array(len(user_id))
arousal_audio = generate_2D_array(len(user_id))
valence_text = generate_2D_array(len(user_id))
arousal_text = generate_2D_array(len(user_id))
valence_fumoji = generate_2D_array(len(user_id))
arousal_fumoji = generate_2D_array(len(user_id))

count = 0
for i in user_id:
    valence_audio[count] = audio_data[audio_data['Talk'] == talk_id][audio_data['UserID'] == i]['Valence'].values
    arousal_audio[count] = audio_data[audio_data['Talk'] == talk_id][audio_data['UserID'] == i]['Arousal'].values
    valence_text[count] = text_data[text_data['Talk'] == talk_id][text_data['UserID'] == i]['Valence'].values
    arousal_text[count] = text_data[text_data['Talk'] == talk_id][text_data['UserID'] == i]['Arousal'].values
    valence_fumoji[count] = fumoji_data[fumoji_data['Talk'] == talk_id][fumoji_data['UserID'] == i]['Valence'].values
    arousal_fumoji[count] = fumoji_data[fumoji_data['Talk'] == talk_id][fumoji_data['UserID'] == i]['Arousal'].values
    count += 1

# plot_figure(valence_audio,'audio','valence')
# plot_figure(arousal_audio,'audio','arousal')

# plot_figure(valence_fumoji,'fumoji','valence')
# plot_figure(arousal_fumoji,'fumoji','arousal')
# plot_figure(valence_text,'text','valence')
# plot_figure(arousal_text,'text','arousal')





