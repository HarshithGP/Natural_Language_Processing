
L = []
#from nltk.corpus import stopwords
import re
with open('lexicon/sports.sports_league') as f:
	for word in f:
		#word=word.lower().replace('[^a-zA-Z0-9 ]','')
		word = re.sub('[^a-zA-Z0-9\n ]', '', word).lower()
		word = word.split()
		for w in word:
			L.append(w)
		
with open('name_lower.txt','w') as op:
	for word in L:
		op.write(word+'\n')

"""
import pandas as pd

new_list=[]
# comapny features
links = (pd.read_csv('data/twitter_test.ner', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist()
for i in links:
    i=i.split('\t')
    j=i[0].split(':')
    if j[0] == 'http':
        new_list.append(i[0])


for k in new_list:
    x=k.split(' ')
    L.append(x[0])

k=new_list[0]
z=k.split("\\s+")

with open('links.txt','w') as f:
    for link in new_list:
        f.write(link)
        f.write('\n')

"""

"""
with open('lexicon/music.lex') as f:
	x=[]
	for word in f:
		if word not in x:
			x.append(word)

with open('name_lower.txt','w') as op:
	for word in x:
		op.write(word)	
 """