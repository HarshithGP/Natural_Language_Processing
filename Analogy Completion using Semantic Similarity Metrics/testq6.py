#!/usr/bin/env python
import distsim
"""
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
king = word_to_vec_dict['king']
man = word_to_vec_dict['man']
woman = word_to_vec_dict['woman']

ret = distsim.show_nearest(word_to_vec_dict,
                           king-man+woman,
                           set(['king','man','woman']),
                           distsim.cossim_dense)
"""

word_to_ccdict = distsim.load_contexts("nytcounts.4k")
king = word_to_ccdict['king']
man = word_to_ccdict['man']
woman = word_to_ccdict['woman']

d = {}
for key1 in king:
	if key1 in man and key1 in woman:
		d[key1]=king.get(key1)-man.get(key1)+woman.get(key1)

ret = distsim.show_nearest(word_to_ccdict,
                           d,
                           set(['king','man','woman']),
                           distsim.cossim_sparse)
print("king : man :: {} : woman".format(ret[0][0]))