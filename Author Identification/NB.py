# Natural Language Processing

# Importing the libraries
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
# Importing the dataset
dataset = pd.read_csv('train.tsv', delimiter = '\t', quoting = 3)

#shakespeare : 0-1854
#Bronte 1855 - 3665
def get_words(start,end):
    S = []
    for i in range(start,end):
        line = dataset['text'][i].lower()
        line = re.sub('[^a-zA-Z]',' ',line)
        line = line.split()
        for word in line:
            if word not in set(stopwords.words('english')):
                S.append(word)
    return S

from nltk.stem.snowball import SnowballStemmer
def snowball_stem(word):
	"""Snowball Stemmer"""
	ss = SnowballStemmer("english", ignore_stopwords=True)
	return ss.stem(word)

from collections import defaultdict
def build_D(S):
    D = defaultdict(int)
    for word in S:
        #word = snowball_stem(word)
        D[word] += 1
    return D

def word_list(D):
    W = []
    poet_words = []
    for w in sorted(D, key=D.get, reverse=True):
        #if D.get(w)<3:
        W.append([w,D.get(w)])
        poet_words.append(w)
    return poet_words, W

     
S_words, S = word_list(build_D(get_words(0,1854)))
B_words, B = word_list(build_D(get_words(1855,3665)))

S_best = []
for word in S:
    if word[0]<5:
        low.append(i[0])
F, freq = word_list(build_D(get_words(0,3665)))
low = []
for i in freq:
    if i[1]<5:
        low.append(i[0])

    
common = []      
common = list(set(S_words).intersection(B_words))   


B_only = list(set(B_words).difference(common))
S_only = list(set(S_words).difference(common))

message = "Hello SeperMan Hi"
print("Capital Letters: ", sum(1 for c in message if c.isupper()))