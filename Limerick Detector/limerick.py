"""
CSCI 544 - Natural Language Processing
University of Southern California,
Fall 2017

HomeWork Assignment 1
Code developed by - HARSHITH GURU PRASAD
CS GRADUATE STUDENT, USC VITERBI
"""

#!/usr/bin/env python
import argparse
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

# Use word_tokenize to split raw text into words
from string import punctuation
#import pronouncing
import nltk
#nltk.download('cmudict')
scriptdir = os.path.dirname(os.path.abspath(__file__))

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

class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        # TODO: provide an implementation!
        word = word.lower()
        D = self._pronunciations
        #D = nltk.corpus.cmudict.dict()
        if(word not in D.keys()):
            #print word not in CMUDictionary
            return 1

        #count stores no of syllables for each pronunciation of the word
        count = []

        #for each pronunciation
        for x in D[word]:
            n = 0
            #for each syllable
            for y in x:
                #if vowel sound
                if y[-1].isdigit():
                    n = n + 1
            count.append(n)
        # return the pronunciation having least syllables
        return min(count)
        #return min([len([y for y in x if y[-1].isdigit()]) for x in D[word.lower()]])

    def rhymes(self, a, b):

        """
               Returns True if two words (represented as lower-case strings) rhyme,
               False otherwise.
        """
        D = self._pronunciations
        a = a.lower()
        b = b.lower()
        # print "----------------------------------"
        # print "Rhyming ",a,b

        if a in D.keys() and b in D.keys():
            a = D[a]
            #print a
            b = D[b]
            #print b

            #stores syllables after the first consonant sound
            last_syl_a = []
            last_syl_b = []

            # for each pronunciation of the word
            for y in a:
                syl = []
                pos = 0
                for i in range(0, len(y)):
                    #if vowel
                    if y[i][-1].isdigit():
                        pos = i
                        break
                # append all syllables from first vowel
                for i in range(pos, len(y)):
                    syl.append(y[i])


                last_syl_a.append(syl)
            # print(last_syl_a)

            # for each pronunciation of the word
            for y in b:
                syl = []
                pos = 0
                for i in range(0, len(y)):
                    # if vowel
                    if y[i][-1].isdigit():
                        pos = i
                        break
                # append all syllables after first consonant sound
                for i in range(pos, len(y)):
                    syl.append(y[i])

                last_syl_b.append(syl)
            # print(last_syl_b)

            if any(i in last_syl_a for i in last_syl_b):
                # print "Rhyming - Yes"
                return True

            else:
                # print "Checking if Shorter word is suffix of Longer word's pronunciation"
                if len(last_syl_a[0]) > len(last_syl_b[0]):
                    big = last_syl_a
                    small = last_syl_b
                else:
                    big = last_syl_b
                    small = last_syl_a

                for i in big:
                    for j in small:
                        count = 0
                        for k in range(0, len(j)):
                            if j[-(k + 1)] == i[-(k + 1)]:
                                count = count + 1
                        if count == len(j) and count > 0:
                            # print "Rhyming - yes", i,j
                            return True

                return False
        else:
            # Either or Both words not in CMU Dictionary
            return False


    def is_limerick(self, text):

        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)

        """
        # TODO: provide an implementation!
        text = text.lower()
        p = []
        p = text.split('\n')
        p = [i.strip(' ') for i in p]
        p = list(filter(None, p))

        # all limericks must have 5 lines AABBA
        if len(p) != 5:
            return False

        #words list stores the list of words in each line of the limerick
        words = []
        for i in range(0, 5):
            p[i] = p[i].strip(".,:;?!")
            temp = []
            T = p[i]
            temp = self.apostrophe_tokenize(T)
            words.append(temp)

        count = []
        #print len(words)
        for i in range(0, 5):
            #print words[i]
            n = 0
            for j in words[i]:
                n = n + self.num_syllables(j)
            count.append(n)

        # check if any line has fewer than 4 syllables
        for i in count:
            if i < 4:
                return False

        A1 = count[0]
        A2 = count[1]
        B1 = count[2]
        B2 = count[3]
        A3 = count[4]

        # check if B1 has fewer syllables than A1, A2 and A3
        if B1 > A1 or B1 > A2 or B1 > A3:
            return False

        # check if B2 has fewer syllables than A1, A2 and A3
        if B2 > A1 or B2 > A2 or B2 > A3:
            return False

        # check if the no of syllables in B1 and B2 differs by more than 2
        if abs(B1 - B2) > 2:
            return False

        # check if any two A's differ in no of syllables by more than 2
        if abs(A1 - A2) > 2 or abs(A1 - A3) > 2 or abs(A2 - A3) > 2:
            return False

        #check if A1, A2 and A3 rhyme with each other
        if self.rhymes(words[0][-1], words[1][-1]) and self.rhymes(words[0][-1], words[4][-1]) and self.rhymes(words[1][-1], words[4][-1]):
            #check if B1 and B2 rhyme with each other
            if self.rhymes(words[2][-1],words[3][-1]):
                #check if A and B do not rhyme
                if (not self.rhymes(words[0][-1], words[2][-1]) and
                        not self.rhymes(words[0][-1], words[3][-1]) and
                        not self.rhymes(words[1][-1], words[2][-1]) and
                        not self.rhymes(words[1][-1], words[3][-1]) and
                        not self.rhymes(words[4][-1], words[2][-1]) and
                        not self.rhymes(words[4][-1], words[3][-1])
                    ):
                    return True

        return False

    def apostrophe_tokenize(self, T):
        T = re.sub('[^a-zA-Z ]', '', T)
        T = word_tokenize(T)
        # print T
        return T

    def guess_syllables(self, word):

        # Guess the number of syllables in a word that may not be present in the CMU dictionary
        D = self._pronunciations

        word = word.lower().strip(".:;?!")
        if word in D.keys():
            print "Word present in CMU Dictionary"
            return self.num_syllables(word)

        # Count the syllables in the word that's not in the Dictionary.
        count = 0
        vowels = 'aeiouy'
        if word[0] in vowels:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                count += 1
        if word.endswith('le'):
            count += 1
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count += 1
        return count

# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")

  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
