"""
CSCI 544 - Natural Language Processing | USC - Fall 2017
Homework Assignment 3
Harshith Guru Prasad
"""

#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
#from nltk.tokenize import word_tokenize
#nltk.download('wordnet')
kTOKENIZER = TreebankWordTokenizer()

import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier

"""
def morphy_stem(word):
	 #Simple stemmer
	stem = wn.morphy(word)
	if stem:
		return stem.lower()
	else:
		return word.lower()

from nltk.stem.porter import PorterStemmer
def porter_stem(word):
	# Porter stemmer#
	ps = PorterStemmer()
	return ps.stem(word).lower()
"""

from nltk.stem.snowball import SnowballStemmer
def snowball_stem(word):
	"""Snowball Stemmer"""
	ss = SnowballStemmer("english", ignore_stopwords=True)
	return ss.stem(word).lower()

"""Feature Generation"""
import pandas as pd
import re
from nltk.corpus import stopwords
dataset = pd.read_csv('train.tsv', delimiter = '\t', quoting = 3)

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

def build_D(S):
	D = defaultdict(int)
	for word in S:
		D[word] += 1
	return D

def word_list(D):
	W = []
	poet_words = []
	for w in sorted(D, key=D.get, reverse=True):
		W.append([w,D.get(w)])
		poet_words.append(w)
	return poet_words, W
 
S_words, S = word_list(build_D(get_words(0,1854)))
B_words, B = word_list(build_D(get_words(1855,3665)))
common = []      
common = list(set(S_words).intersection(B_words))   


from nltk.util import ngrams
from collections import Counter
class FeatureExtractor:
	def __init__(self):
		"""
		You may want to add code here
		"""

		None

	def features(self, text):
		d = defaultdict(int)

		for i in range(0,len(text)):
			if text[len(text)-1] ==" ":
				d['xSpace']+=1
		
		for i in range(0,len(text)):
			#if text[len(text)-1] in ['!','?',';',':'] and text[len(text)-2] ==" " :
				#d['punc']+=1
			if text[i] in ['0','1','2','3','4','5','6','7','8','9']:
				d['numChar']+=1
		
		text = re.sub('[^a-zA-Z]',' ',text)
		text=text.lower()
		d['No_Of_Words']=len(text.split())
		
		bigrams = ngrams(text.split(), n=2)
		d['Bigrams'] = len(Counter(bigrams))

		"""
		trigrams = ngrams(text.split(), n=3)
		for grams in trigrams:
  			d[grams]+=1
  		"""

		for ii in kTOKENIZER.tokenize(text):
			if not ii in set(stopwords.words('english')):
				d[snowball_stem(ii)] += 1
			#T = nltk.pos_tag(ii)
			#d[T[0][1]] += 1 

			if ii in S_words:
				d['S_H']+=2
			if ii in B_words:
				d['E_B']+=2
			if ii in common:
				d['S_H']-=1
				d['E_B']-=1
			
		return d

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
	fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
	if code.startswith('r'):
	  ret = reader(fh)
	elif code.startswith('w'):
	  ret = writer(fh)
	else:
	  sys.stderr.write("I didn't understand code "+code+"\n")
	  sys.exit(1)
  return ret

if __name__ == "__main__":
	
	import argparse

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
	parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
	parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
	parser.add_argument('--subsample', type=float, default=1.0,
						help='subsample this fraction of total')
	args = parser.parse_args()
	trainfile = prepfile(args.trainfile, 'r')
	if args.testfile is not None:
		testfile = prepfile(args.testfile, 'r')
	else:
		testfile = None
	outfile = prepfile(args.outfile, 'w')

	# Create feature extractor (you may want to modify this)
	fe = FeatureExtractor()
	
	# Read in training data
	train = DictReader(trainfile, delimiter='\t')
	
	# Split off dev section
	dev_train = []
	dev_test = []
	full_train = []

	i=1
	for ii in train:
		if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
			continue
		feat = fe.features(ii['text'])

		if int(ii['id']) % 5 == 0:
			dev_test.append((feat, ii['cat']))
		else:
			dev_train.append((feat, ii['cat']))
		full_train.append((feat, ii['cat']))

	# Train a classifier
	sys.stderr.write("Training classifier ...\n")
	classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

	right = 0
	total = len(dev_test)
	for ii in dev_test:
		prediction = classifier.classify(ii[0])
		if prediction == ii[1]:
			right += 1
	sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))
	#classifier.show_most_informative_features(500)
	#features = classifier.most_informative_features(500)
	#print features


	if testfile is None:
		sys.stderr.write("No test file passed; stopping.\n")
	else:
		# Retrain on all data
		classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

		# Read in test section
		test = {}
		for ii in DictReader(testfile, delimiter='\t'):
			test[ii['id']] = classifier.classify(fe.features(ii['text']))

		# Write predictions
		o = DictWriter(outfile, ['id', 'pred'])
		o.writeheader()
		for ii in sorted(test):
			o.writerow({'id': ii, 'pred': test[ii]})
	