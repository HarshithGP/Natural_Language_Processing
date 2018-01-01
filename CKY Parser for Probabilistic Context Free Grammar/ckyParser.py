import sys
import codecs
if sys.version_info[0] == 2:
    from itertools import izip
else:
    izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

#scriptdir = os.path.dirname(os.path.abspath(__file__))
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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
    ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
    group = parser.add_mutually_exclusive_group()
    dest = arg if dest is None else dest
    group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
    group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)

from tree import TreeG
from collections import defaultdict
import re
import itertools
import math

from nltk.stem.snowball import SnowballStemmer
def snowball_stem(word):
    """Snowball Stemmer"""
    ss = SnowballStemmer("english", ignore_stopwords=True)
    return ss.stem(word)

class CKYParser:
    
    def __init__(self, text):
        
        #production set of all rules in the pCFG
        self.allProds = set()
        #set of all Non Terminal Symbles in the pCFG           
        self.nonTerms = set()        
        #probabilities for all productions - MLE
        self.Prob = defaultdict(float)  
         #matrix storing DP results  
        self.DP_values = defaultdict(float)
        #backtracking to determine the parent
        self.backPointers = {}
        #maps best non terminal to terminal ("word")           
        self.terminals = {} 
        #the list of words             
        self.text = text.split()
        #list of words to be replaced by unk at parse time     
        self.origText = list(self.text)  

        #Use trainDict to keep track of words that occur multiple time and replace words with freq <=1 with <unk>
        multiWords = []
        stemmed = []

        trainDict = open('MultiWord.txt')
        many_words = trainDict.readlines()
        for word in many_words:
            multiWords.append(word.strip())
            if snowball_stem(word) in ['ing', 'er', 'es', 'ies', 'ple']:
                stemmed.append('<unk>'+snowball_stem(word.strip()))

        #store words with freq<=1 for postprocessing
        for i,word in enumerate(self.text):
            if word not in multiWords:
                self.text[i] = "<unk>"
      
        self.n = len(self.text)

    def addUnary(self,begin, end):
        #Adds unary rules into the table
        for Y in self.nonTerms:
            for Z in self.nonTerms:
                if (Y,Z) in self.allProds:
                    prob = self.Prob[(Y,Z)] * self.DP_values[(begin,end,Z)]
                    #update best
                    if prob > self.DP_values[(begin,end,Y)]:
                        self.DP_values[(begin, end, Y)] = prob
                        self.backPointers[(begin, end, Y)] = (Z,) 

    def backtrack_init(self, n):
       #Initialize backtrack
        size = n 
        if (0,size,'TOP') not in self.backPointers:
            #print "NONE"
            return None
        t = self.Recursive_Backtrack((0,size,'TOP'))
        t.deBinarize()
        return t

    def Recursive_Backtrack(self, next):
        #Recursive function for backtracking. 
        first = next[0]
        last = next[1]
        label = next[2]

        #check for parents of subtrees recursively
        if not next in self.backPointers:
            if next in self.terminals:
                word = self.origText[next[0]]
                t = TreeG(label=label, subs = None, wrd=word, span=(first, last))
            return t
        
        #branches is of the form [X, i, j]
        branches = self.backPointers[next]

        if len(branches) > 0 and len(branches) < 2:
            next = (first, last, branches[0])

            t1 = self.Recursive_Backtrack(next)
            t = TreeG(label=label, subs = [t1], wrd=None, span=t1.span)
            return t

        elif len(next) > 2 and len(next) < 4:
            (split, left, right) = branches
            next_left = (first, split, left)
            next_right = (split, last, right)

            t1 = self.Recursive_Backtrack(next_left) #left side    
            t2 = self.Recursive_Backtrack(next_right) #right side

            #span of tree X
            t = TreeG(label=label, subs = [t1,t2], wrd=None, span=(t1.span[0], t2.span[1]))
            return t

    def parse(self):
        '''
        CKY Algorithm, Production: A -> w_i,  A -> B C,  A -> B
        Use backtrack to find the best tree and return it
        '''
        for line in open(sys.argv[4]):
            rule = re.split(r"\-\>|\#", line.strip())
            p = rule[0].strip()
            q = rule[1].strip()
            prob = float(rule[2].strip())
            self.nonTerms.add(p)
            self.allProds.add((p,q))
            self.Prob[(p,q)] = prob
            
        self.nonTerms = sorted(list(self.nonTerms))
        size = self.n
        # map pre terminals X -> w_i
        for ptr in range(0,size):
            begin = ptr
            end = ptr + 1
            for A in self.nonTerms:
                word = self.text[begin]
                if (A,word) in self.allProds:
                    self.DP_values[(begin,end,A)] = self.Prob[(A, word)]
                    self.terminals[(begin,end,A)] = word
            self.addUnary(begin,end)

        #Actual CKY algorithm
        index = 0
        for span in range(index+2,size+1):
            for begin in range(index,size-span+1):
                end = begin + span
                for split in range(begin+1,end):
                    for A,X in self.allProds:
                        # X is a pair of prodcutions, A -> X where X = L R
                        rhs = X.split()
                        if len(rhs)>1 and len(rhs) <3:
                            B = rhs[0].strip()
                            C = rhs[1].strip()
                            #parse probability of tree rooted at A at begin,end if left, right are B and C
                            prob = self.DP_values[(begin,split,B)] * self.DP_values[(split, end, C)] * self.Prob[(A, X)]
                            if prob > self.DP_values[(begin, end,  A)]:
                                self.DP_values[(begin, end, A)] = prob
                                self.backPointers[(begin, end, A)] = (split, B, C)
                self.addUnary(begin,end)

        #finished DP algo, find best tree
        best_tree = self.backtrack_init(len(self.text))

        if best_tree is not None:
            s = str(best_tree)
            return s
        else:
            s = "NONE"
            return s

#from sklearn.linear_model import LinearRegression
#import matplotlib.pyplot as plt
import argparse
import time
def main():
    parser = argparse.ArgumentParser(description="trivial right-branching parser that ignores any grammar passed in",
                                                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input (one sentence per line strings) file")
    parser.add_argument("--grammarfile", "-g", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="grammar file; ignored")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output (one tree per line) file")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    #workdir = tempfile.mkdtemp(prefix=os.path.basename(__file__), dir=os.getenv('TMPDIR', '/tmp'))

    """
    def cleanwork():
        shutil.rmtree(workdir, ignore_errors=True)
    if args.debug:
        print(workdir)
    else:
        atexit.register(cleanwork)
    """
    infile = prepfile(args.infile, 'r')
    outfile = prepfile(args.outfile, 'w')
    
    """
    #PLOT : Parse Time vs Sentence Length 
    i=0
    x_axis = []
    y_axis = []
    plt.title('Parsing Time vs Sentence Length (logScaled)')
    plt.xlabel('No of Words')
    plt.ylabel('Time (s)')
    plt.xscale('log')
    plt.yscale('log')
    """
    for line in infile:
        # start time
        #t1 = time.time()
        #n = len(line.split())
        #x_axis.append(n)
     
        s = CKYParser(line.strip())
        outfile.write(s.parse())
        outfile.write('\n')
        
        """
        if i == 0:
            print("First Line of Dev Strings: "+line)
            print("Parse Tree : "+str(s.compute()))
            print("\nLog Probability = "+str(math.log10(1.79932e-18)))
            i=1
       """

        #finish time
        #t2 = time.time()-t1
        #y_axis.append(t2)

    #plt.scatter(x_axis, y_axis)
    #plt.show()
    #print(x_axis)
    #print(y_axis)

if __name__ == "__main__":
    main()
    