#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import math
from nltk.stem.snowball import SnowballStemmer
ss = SnowballStemmer("english")

def syn_matches(h, ref):
    
    val = 0
    
    length = abs(len(h)-len(ref))
    if length <= 3:
        val=val+1
    
    h=[re.sub('[^a-zA-Z0-9-]','',word.lower()) for word in h]
    ref=[re.sub('[^a-zA-Z0-9-]','',word.lower()) for word in ref]

    val+=(sum(1 for w in h if w in ref))

    for w in h:
        syn=[x.name().split(".")[0] for x in wn.synsets(w)]
        if set(syn).intersection(ref):
            val=val+1 
    """
    stems = [ss.stem(word) for word in ref]
    for w in h:
         val+=(sum(1 for w in h if ss.stem(w) in stems))
    """
    return val

def word_matches(h, ref):
    
    #h = [word.lower() for word in h if not word in set(stopwords.words('english'))]
    #ref = [word.lower() for word in ref if not word in set(stopwords.words('english'))]
    
    ref=[word.lower() for word in ref]
    h=[word.lower() for word in h]
    x=0.90
    if sum(1 for w in h) == 0:
        return 0
    
    P = float(sum(1 for w in h if w in ref)) / sum(1 for w in h)
    R = float(sum(1 for w in h if w in ref)) / sum(1 for w in ref)
    N = P*R
    D = (x*P)+(1-x)*R
    
    if P>0 and R>0:
        chunks = sum(1 for w in ref if w not in h)
        unigrams = sum(1 for w in h if w in ref)
        penalty = 0.5 * float(chunks)/unigrams
        F = float(N)/D
        val = (1-penalty)*F
        return val
    else:
        return 0
   
def bleu(h, ref):

    #ref=[re.sub('[^a-zA-Z0-9-]','',word.lower()) for word in ref]
    #h=[re.sub('[^a-zA-Z0-9-]','',word.lower()) for word in h]
   
    #ref=[word.lower() for word in ref]
    #h=[word.lower() for word in h]
    
    r=len(ref)
    c=len(h)
    if(c==0):
        return 0

    if c>r:
        BP = 1
    else:
        BP = math.exp(1-float(r)/c)

    ref_bigrams = zip(ref, ref[1:])
    ref_trigrams = zip(ref, ref[1:], ref[2:])
    ref_quadgrams = zip(ref, ref[1:], ref[2:], ref[3:])

    hyp_bigrams = zip(h, h[1:])
    hyp_trigrams = zip(h, h[1:], h[2:])
    hyp_quadgrams = zip(h, h[1:], h[2:], h[3:])

    #if len(hyp_bigrams)==0 or len(hyp_trigrams)==0 or len(hyp_quad:
        #return 0

    unigram_precision = float(len(set(h).intersection(set(ref))))/c
    bigram_precison = float(1+len(set(ref_bigrams).intersection(set(hyp_bigrams))))/(len(hyp_bigrams)+1)
    trigram_precison = float(1+len(set(ref_trigrams).intersection(set(hyp_trigrams))))/(len(hyp_trigrams)+1)
    quadgram_precision = float(1+len(set(ref_quadgrams).intersection(set(hyp_quadgrams))))/(len(hyp_quadgrams)+1)
    #print(quadgram_precision)

    mean = unigram_precision * bigram_precison * trigram_precison * quadgram_precision
    mean = mean ** (1.0/4)
    mean = BP * mean
    return mean

def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
            help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()
 
    # we create a generator and avoid loading all sentences into a list
    def sentences():
        
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
                """
                h = []
                pair=pair.split('|||')
                for sentence in pair:
                    sentence=re.sub('[^a-zA-Z ]','',sentence).split()
                    h.append(sentence)
                yield h
                """
                   #yield [re.sub('[^a-zA-Z ]','',sentence).split() for sentence in pair.split(' ||| ')]
    
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        rset = ref
        
        #h1_match = word_matches(h1, rset)
        #h2_match = word_matches(h2, rset)

        M1_h1 = word_matches(h1, rset)
        M1_h2 = word_matches(h2, rset)

        M2_h1 = bleu(h1, rset)
        M2_h2 = bleu(h2, rset)

        M3_h1 = syn_matches(h1, rset)
        M3_h2 = syn_matches(h2, rset)

        H1 = M1_h1 + M2_h1 + M3_h1
        H2 = M1_h2 + M2_h2 + M3_h2
       
        print(1 if H1 > H2 else # \begin{cases}
                (0 if H1 == H2
                    else -1)) # \end{cases}

        
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
