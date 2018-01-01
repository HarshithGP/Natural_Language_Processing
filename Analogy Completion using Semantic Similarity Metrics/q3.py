#!/usr/bin/env python
import distsim

word_to_ccdict = distsim.load_contexts("nytcounts.4k")
words = ['jack','elizabeth','europe','canada','doctor','champions','driving','laughed']
for each_word in words:   
    print("Word : "+each_word)
    print("-------------------------------------")
    for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict[each_word], set([each_word]), distsim.cossim_sparse), start=1):
        print("{}: {} ({})".format(i, word, score))
    print("-------------------------------------")