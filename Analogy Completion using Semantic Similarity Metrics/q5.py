#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

words = ['jack','elizabeth','europe','canada','doctor','champions','driving','laughed']
for each_word in words:   
    print("Word : "+each_word)
    print("-------------------------------------")
    for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict[each_word], set([each_word]), distsim.cossim_dense), start=1):
        print("{}: {} ({})".format(i, word, score))
    print("-------------------------------------")