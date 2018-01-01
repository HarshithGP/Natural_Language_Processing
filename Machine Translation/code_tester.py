"""
from nltk.corpus import wordnet as wn
import re
h=[x.name().split(".")[0] for x in wn.synsets('furious')]

g=['m,ad','s.Ad','an]gry,']
g=[re.sub('[^a-zA-Z0-9-]','',word.lower()) for word in g]
print(g)
"""

import math

input_list = ['the', 'champions', 'league', 'proved', 'we', 'could', 'hold', 'our', 'own']
bigrams = zip(input_list, input_list[1:])
trigrams = zip(input_list, input_list[1:], input_list[2:])
quadgrams = zip(input_list, input_list[1:], input_list[2:], input_list[3:])

machine = ['we', 'have', 'proven', 'in', 'the', 'champions', 'league', 'that', 'we', 'can', 'respond', 'to', 'modern', 'challenges']
hyp_bigrams = zip(machine, machine[1:])
hyp_trigrams = zip(machine, machine[1:], machine[2:])
hyp_quadgrams = zip(machine, machine[1:], machine[2:], machine[3:])

if len(hyp_bigrams)==0 or len(hyp_trigrams)==0 or len(hyp_quadgrams)==0:
        mean=0
try:
	unigram_precision = float(len(set(input_list).intersection(set(machine))))/len(machine)
	bigram_precison = float(len(set(bigrams).intersection(set(hyp_bigrams))))/len(hyp_bigrams)
	trigram_precison = float(len(set(trigrams).intersection(set(hyp_trigrams))))/len(hyp_trigrams)
	#quadgram_precision = float(len(set(quadgrams).intersection(set(hyp_quadgrams))))/len(hyp_quadgrams)
	mean = unigram_precision * bigram_precison * trigram_precison 
	mean = mean ** (1.0/3)
	r=len(input_list)
	c=len(machine)
	if c>r:
	        BP = 1
	else:
	        BP = math.exp(1-float(r)/c)

	mean = mean * BP
	print(mean)
except:
	print("0")

