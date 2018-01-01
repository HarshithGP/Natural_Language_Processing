from __future__ import division
import sys,json,math
import os
import numpy as np
from collections import defaultdict

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1
    
    """
        Find sum of products of values of corresponding contexts for both words
        Multiply counts of common contexts
        Products of uncommon contexts will be 0 and not contribute to the sum 
    """
    Numerator = 0
    for key1 in v1:
        for key2 in v2:
            if(key1 == key2):
                # if the contexts for the two words are the same, their counts are multiplied
                Numerator += v1.get(key1)*v2.get(key2)
    """            
    sum1=0
    sum2=0
    for key1 in v1:
        for key2 in v2:
            if(key1 == key2):
                sum1+=v1.get(key1)*v1.get(key1)
                sum2+=v2.get(key2)*v2.get(key2)
    normWord1 = math.sqrt(sum1)
    normWord2 = math.sqrt(sum2)
    Denominator = normWord1*normWord2
    """
    # finding normalized sum for of squares for the first word
    
    sum = 0
    for key in v1:
        sum += v1.get(key)*v1.get(key)
    normWord1 = math.sqrt(sum)
    
    # finding normalized sum for of squares for the second word    
    sum = 0
    for key in v2:
        sum += v2.get(key)*v2.get(key)
    normWord2 = math.sqrt(sum)
   
    Denominator = normWord1*normWord2
    CosSim = Numerator/Denominator
    return CosSim 
    

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    """
    numerator = np.sum(v1*v2)
    norm_d1 = np.sqrt(np.sum(np.square(v1)))
    norm_d2 = np.sqrt(np.sum(np.square(v2)))
    denominator = norm_d1 * norm_d2
    
    CosSim = numerator/denominator
    return CosSim
    """
    return np.sum(v1*v2)/(np.sqrt(np.sum(np.square(v1)))*np.sqrt(np.sum(np.square(v2))))

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    
    #compute similarity scores for all remaining words wrt to w_vec
    Dscore = defaultdict(int)
    for key in word_2_vec.keys():
    	if key not in list(exclude_w):     
        		Dscore[key] = sim_metric(w_vec,word_2_vec.get(key))
        		
    L=[]
    count=0
    for w in sorted(Dscore, key=Dscore.get, reverse=True):
        if count<10:
            tup=(w, Dscore.get(w))
            L.append(tup)
            count+=1
        else:
            break
    return L

def cossim_jacard(v1,v2): 
    numerator = np.sum(np.minimum(v1,v2))
    denominator = np.sum(np.maximum(v1,v2))
    JacSim = numerator/denominator
    return JacSim

def cossim_dice(v1,v2):
    numerator = np.sum(np.minimum(v1,v2))
    denominator = np.sum(v1+v2)
    DiceSim = (2*numerator)/denominator
    return DiceSim