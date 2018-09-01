import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mimicry_analyser import MimiAnalyser

ma = MimiAnalyser('data/test_data_pure.csv')


#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]

data = pd.read_csv('data/test_data_pure.csv')

text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

fumoji_valence_error = [{} for i in range(12)]
text_valence_error = [{} for j in range(12)]

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
    plt.figure(figsize = (28.8, 16.39))
    plt.title('conversation {} {} {} trace'.format(talk_id[index],name,type))
    for i in range(len(array)):
        plt.plot(array[i],label = 'userid {}'.format(user_id[index][i]))
    array = pd.DataFrame(array)
    plt.plot(array.apply(np.mean, axis = 0), label = 'average')
    plt.legend()
    # plt.show()
    plt.savefig('c{}{}{}'.format(talk_id[index],name,type))

def plot_custome(norm_data, df, talk, va):
    plt.figure(figsize = (28.80, 16.39))
    plt.title('conversation {} {} {}'.format(talk,'audio',va))

    plt.plot(df.loc[12],label = 'userid 31')
    plt.plot(df.loc[0],label = 'userid 32')
    plt.plot(df.loc[1],label = 'userid 19')
    # plt.plot(df.loc[8],label = 'userid 42')        
    # plt.plot(df.loc[9],label = 'userid 43')
    # plt.plot(df.loc[10],label = 'userid 44')
    # plt.plot(df.loc[14],label = 'userid 48')
    plt.plot(norm_data,label = 'userid average')
        
    plt.legend()
    # plt.show()  
    plt.savefig('c{}{}{}'.format(talk,'A',va))  

#calculate the k values of each segment
def get_k_value(df):
    frameK = np.zeros((df.shape[0], df.shape[1]-1))
    for index, row in df.iterrows():
        a = row[0]
        for index_, item in row.iteritems():
            if index_ > 0:
                frameK[index][index_ - 1] = item - a
                a = item
    return pd.DataFrame(frameK)

#calculate the mean value of each conversation
def k_error(frameK, k_mean):
    k_err = np.zeros(frameK.shape[0])
    for index, row in frameK.iterrows():
        for index_, item in row.iteritems():
            k_err[index] += np.square(item - k_mean[index_])
        k_err[index] = np.sqrt(k_err[index])
    return k_err

def get_correlation(array):
    correlations = np.zeros(len(array.index))
    for index, row_i in array.iterrows():
        row_i = pd.Series(row_i)
        # print(index, row_i)
        for index2, row_j in array.iterrows():
            row_j = pd.Series(row_j)
            # print(row_j)
            correlations[index] += row_i.corr(row_j)
    return correlations

def get_quadrant(df):
    quadrant = np.zeros(df.shape)
    for index, row_i in df.iterrows():
        row_i = pd.Series(row_i)
        for index2, item in row_i.iteritems():
            if item < 0:
                quadrant[index][index2] = -1
            elif item > 0:
                quadrant[index][index2] = +1
    quadrant = pd.DataFrame(quadrant)
    return quadrant

def quadrant_correction(norm_list, test_list):
    correct_count = 0
    for index, item in norm_list.iteritems():
        if (item * test_list[index] > 0) or (item == test_list[index]):
           correct_count += 1
    return correct_count/len(norm_list)

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



the_talk = 12
df_v = pd.DataFrame(valence_audio_all[the_talk - 2])
df_a = pd.DataFrame(arousal_audio_all[the_talk - 2])
average_v = df_v.apply(np.mean, axis = 0)
average_a = df_a.apply(np.mean, axis = 0)



# get quadrant error
df_v_quadrant = get_quadrant(df_v)
overall_quadrant_v = df_v_quadrant.apply(np.mean, axis = 0)
df_a_quadrant = get_quadrant(df_a)
overall_quadrant_a = df_a_quadrant.apply(np.mean, axis = 0)

cor_arr_v = []
cor_arr_a = []

for index, r in df_v.iterrows():
    cor_arr_v.append(quadrant_correction(overall_quadrant_v, r))
for index, r in df_a.iterrows():
    cor_arr_a.append(quadrant_correction(overall_quadrant_a, r))
    
quadrant_correction_v = pd.Series(cor_arr_v, index = user_id[the_talk-2]).sort_values()
quadrant_correction_a = pd.Series(cor_arr_a, index = user_id[the_talk-2]).sort_values()

#get k value error
dfk_v = get_k_value(df_v)
dfk_v = get_quadrant(dfk_v)
mean_k_v = dfk_v.apply(np.mean, axis = 0)
dfk_a = get_k_value(df_a)
dfk_a = get_quadrant(dfk_a)
mean_k_a = dfk_a.apply(np.mean, axis = 0)

cor_arr_v_2 = []
cor_arr_a_2 = []

for index, r in dfk_v.iterrows():
    cor_arr_v_2.append(quadrant_correction(mean_k_v, r))

for index, r in dfk_a.iterrows():
    cor_arr_a_2.append(quadrant_correction(mean_k_a, r))

k_correction_v = pd.Series(cor_arr_v_2, index = user_id[the_talk-2]).sort_values()
k_correction_a = pd.Series(cor_arr_a_2, index = user_id[the_talk-2]).sort_values()

print(quadrant_correction_v, quadrant_correction_a, k_correction_v, k_correction_a)
# for col in df_v_quadrant:
#     print(df_v_quadrant[col].describe())
# for i in range(1):
#     plot_figure(valence_audio_all[i],'audio','valence',i)
#     plot_figure(arousal_audio_all[i],'audio','arousal',i)

print(pd.Series(user_id[the_talk - 2]))

plot_figure(valence_audio_all[the_talk-2],'audio','valence',the_talk-2)
plot_figure(arousal_audio_all[the_talk-2],'audio','arousal',the_talk-2)

# plot_custome(overall_quadrant_v, df_v, the_talk)
# plot_custome(overall_quadrant_a, df_a, the_talk)

# plot_custome(average_v, df_v, the_talk, 'v')
# plot_custome(average_a, df_a, the_talk, 'a')


