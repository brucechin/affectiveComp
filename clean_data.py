import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data/test_data_filtered.csv')
text_data = data[data['Type'] == 'text']
fumoji_data = data[data['Type'] == 'Fumoji']
audio_data = data[data['Type'] == 'Audio']

def clean_outliner(data):
    talks = [2,3,4,5,6,7,8,9,10,11,12,13]
    talk_length = [52,22,9,11,30,45,4,19,10,32,43,19]
    data_to_concat = []
    for talk in talks:
        for i in range(1,talk_length[talk-2]+1):
            valence = data[data['Talk'] == talk][data['Sentence'] == i].sort_values(by = 'Valence')
            arousal = data[data['Talk'] == talk][data['Sentence'] == i].sort_values(by = 'Arousal')
            length = len(valence['ID'])
            if(length > 0):
                valence_upperquartile = valence.iloc[int(length * 3 / 4)]['Valence']
                valence_lowerquartile = valence.iloc[int(length * 1 / 4)]['Valence']
                valence = valence[valence['Valence'] < valence_upperquartile + 1.5 * (valence_upperquartile - valence_lowerquartile)]
                valence = valence[valence['Valence'] > valence_lowerquartile - 1.5 * (valence_upperquartile - valence_lowerquartile)]
                arousal_upperquartile = arousal.iloc[int(length * 3 / 4)]['Arousal']
                arousal_lowerquartile = arousal.iloc[int(length * 1 / 4)]['Arousal']
                valence = valence[valence['Arousal'] < arousal_upperquartile + 1.5 * (arousal_upperquartile - arousal_lowerquartile)]
                valence = valence[valence['Arousal'] > arousal_lowerquartile - 1.5 * (arousal_upperquartile - arousal_lowerquartile)]
                data_to_concat.append(valence)
    return pd.concat(data_to_concat,axis = 0)



audio_data = clean_outliner(audio_data)
text_data = clean_outliner(text_data)
fumoji_data = clean_outliner(fumoji_data)


print(text_data.describe())
print(fumoji_data.describe())
print(audio_data.describe())

