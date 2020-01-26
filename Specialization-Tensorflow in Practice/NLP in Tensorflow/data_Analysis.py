'''
To clarify doubts related to NLP in Tensorflow course
'''
from collections import defaultdict
import numpy as np

input_sequences=np.array([[120,2,5,43,4],[12,32,55,47,45]])
'''
[:,:-1] means all rows and all but last column elements
[:,-1] means last column element of all rows  
'''
predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
print(predictors)
print(label)

collections_list=[['1234',{'barcodeName':'Monte2 Parlo'}],['1234',{'barcodeName':'Monte Parlo'}],['1234',{'barcodeName':'Monte Parlo'}],
                  ['12345',{'barcodeName':'Monte2 Parlo'}],['12345',{'barcodeName':'Monte2 Parlo'}],['12345',{'barcodeName':'Monte Parlo'}]]
freq_dict={}
for [a,b] in collections_list:
    if 'barcodeName' in b:
        key=b['barcodeName']
        freq_dict[key]=freq_dict.get(key,0)+1
print(freq_dict)
