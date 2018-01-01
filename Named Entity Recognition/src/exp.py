L = []
with open('data/twitter_test.ner') as f:
	for word in f:
		L.append(word)

with open('name_lower.txt','w') as op:
	for word in L:
		op.write(word)

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