#按斜率来分析

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#talk : 2-13
talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]#每段话有多少句话
talk_id = [2,3,4,5,6,7,8,9,10,11,12]
data = pd.read_csv('data/test_data_pure.csv')


text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

user_data = pd.read_csv('data/users.csv')

male_id = user_data[user_data['性别'] == '男']['ID'].values
female_id = user_data[user_data['性别'] == '女']['ID'].values

