import pandas as pd
import numpy as np
import os
from mimicry_analyser import MimiAnalyser

class Annotation(object):
    def __init__(self):
        super(Annotation, self).__init__()
        self.talk_id = [2,3,4,5,7,8,9,10,11,12,13]
        self.anno = {}
        for i in os.listdir('./annotation'):
            if i == '.DS_Store':
                pass
            else:
                talkid = int(i.split('.')[0][4:])
                data = pd.read_csv('./annotation/'+i)
                self.anno[talkid] = data
        self.ma = MimiAnalyser('./data/test_data_filtered.csv')
        self.data = self.ma.data
        self.type_dict = {'说话人性别':['男','女'],
                        '句式':['肯定句','反问句','疑问句','否定句','祈使句'],
                        '文本有无语气词':['有','无'],
                        '单句情绪起伏':['正常','起伏大'],
                        '音量大小':['变大','正常']}
    '''
    返回audio/text/fumoji 对应标注下的VA数组，格式为
    {
          'audio':[[],[],[]],
          'text':[[],[],[]],
          'fumoji':[[],[],[]]
    }
    '''
    def get_VA_by_annotation(self,type,condition): #type有‘说话人性别’，‘句式’，‘文本有无语气词’等，condition为type的具体类别
        type_dic = self.type_dict
        result = {
                  'audio':[],
                  'text':[],
                  'fumoji':[]
                  }
        for i in type_dic.keys():
            if(i == type): #确定根据哪种标注来返回数据
                condition_list  = type_dic[i]
                for j in condition_list:
                    if(j == condition):
                        for talk in self.talk_id:
                            annotation = self.anno[talk]
                            data = self.data[self.data['Talk'] == talk]
                            sentences = annotation[annotation[type] == condition].index.values
                            for sentence in sentences:
                                result['text'].extend(data[data['Sentence'] == sentence][data['Type'] =='text'][['Valence','Arousal']].values)
                                result['fumoji'].extend(data[data['Sentence'] == sentence][data['Type'] =='Fumoji'][['Valence','Arousal']].values)
                                result['audio'].extend(data[data['Sentence'] == sentence][data['Type'] =='Audio'][['Valence','Arousal']].values)

        return result
    '''
    返回对应标注下的(Talk, Sentence)，格式为
    {
        'talkid0':[sentence0, sentence1....]
        'talkid1':[sentence0, sentence1....]
        ...
    }
    '''
    def getTalkSentenceByAnnotation(self, annotation_type, annotation_value):
        result = {}
        for talk in self.talk_id:
            annotation = self.anno[talk]
            sentences = annotation[annotation[annotation_type] == annotation_value].index
            result[talk] = sentences
        return pd.Series(result)




# a = Annotation()
# print(a.getTalkSentenceByAnnotation('文本有无语气词','有'))