#!/usr/bin/env python

import sys, fileinput
import collections
import tree

count = collections.defaultdict(int)
f = open('train.trees.pre.unk', 'w')
trees = []
for line in fileinput.input():
    t = tree.Tree.from_str(line)
    for leaf in t.leaves():
        count[leaf.label] += 1
    trees.append(t)

multi = []
for t in trees:
    for leaf in t.leaves():
        if count[leaf.label] < 2:
            leaf.label = "<unk>"
        elif leaf.label not in multi:
            multi.append(leaf.label)

    #sys.stdout.write("{0}\n".format(t))
    f.write(str(t))
    f.write('\n')
f.close() 

f1 = open('MultiWord.txt','w')
for word in multi:
    f1.write(word) 
    f1.write('\n') 
f1.close()