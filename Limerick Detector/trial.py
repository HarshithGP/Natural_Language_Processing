
import pronouncing
import nltk
#nltk.download('punkt')
import re
#nltk.download('cmudict')
from nltk.tokenize import word_tokenize, sent_tokenize


def Dictionary():
    D = nltk.corpus.cmudict.dict()
    return D

def rhyme_old(a,b):

     a = a.lower()
     b = b.lower()

     D = Dictionary()
     #keys = [ k for k in D.keys() [: len(D)-1]]
     if a in D.keys() and b in D.keys():
        a = D[a]
        print a
        b = D[b]
        print b

        last_syl_a = []
        last_syl_b = []

        for y in a:
            syl = []
            for x in reversed(y):
                if x[-1].isdigit():
                    syl.append(x)
                    break
                else:
                    syl.append(x)
            last_syl_a.append(list(reversed(syl)))
        print(last_syl_a)

        for y in b:
            syl = []
            for x in reversed(y):
                if x[-1].isdigit():
                    syl.append(x)
                    break
                else:
                    syl.append(x)
            last_syl_b.append(list(reversed(syl)))
        print(last_syl_b)

        return any(i in last_syl_a for i in last_syl_b)

     else:
         return False

def num_syl(word):

    D = nltk.corpus.cmudict.dict()
    word = word.lower()
    #print D[word]
    if word not in D.keys():
        #print "Word not in CMU Dictionary"
        return 1

    count = []
    for x in D[word]:
        #print x
        n = 0
        for y in x:
            #print y
            if y[-1].isdigit():
                n = n + 1
        count.append(n)
    #print count
    return min(count)


def apostrophe_tokenize(T):
    T = re.sub('[^a-zA-Z ]','',T)
    T = word_tokenize(T)
    #print T
    return T

def limerick(text):

    text = text.lower()
    print text
    p = []
    p = text.split('\n')
    #print p
    p = [i.strip(' ') for i in p]
    #print p
    p = list(filter(None, p))
    print p
    #print len(p)
    if len(p) != 5:
        return False

    # words is a list that stores a list of words in each line
    words = []
    for i in range(0,5):
        p[i] = p[i].strip(".,:;?!")
        print p[i]
        temp = []
        T = p[i]
        #temp = word_tokenize(T)
        temp = apostrophe_tokenize(T)
        words.append(temp)

    count = []
    print len(words)
    for i in range(0,5):
        print words[i]
        n = 0
        for j in words[i]:
            n = n + num_syl(j)
        count.append(n)
    print count

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

    print "all pre conditions check"

    # check if A1, A2 and A3 rhyme with each other
    if rhyme(words[0][-1], words[1][-1]) and rhyme(words[0][-1], words[4][-1]) and rhyme(words[1][-1],words[4][-1]):
        # check if B1 and B2 rhyme with each other
        if rhyme(words[2][-1], words[3][-1]):
            # check if A and B do not rhyme
            if ( not rhyme(words[0][-1], words[2][-1]) and
                 not rhyme(words[0][-1], words[3][-1]) and
                 not rhyme(words[1][-1], words[2][-1]) and
                 not rhyme(words[1][-1], words[3][-1]) and
                 not rhyme(words[4][-1], words[2][-1]) and
                 not rhyme(words[4][-1], words[3][-1])
                ):
                return True

    return False


def prep_text(a):

    temp = []
    p = a.split('\n')
    p = list(filter(None, p))
    print len(p)
    print p
    for i in p:
        print i


def rhyme_otherOld(a, b):

    a = a.lower()
    b = b.lower()
    #print "----------------------------------"
    print "Rhyming ",a,b
    D = Dictionary()
    if a in D.keys() and b in D.keys():
        a = D[a]
        print a
        b = D[b]
        print b

        last_syl_a = []
        last_syl_b = []

        for y in a:
            syl = []
            pos = 0
            for i in range(0,len(y)):
                if not y[i][-1].isdigit():
                    pos = i
                    break
            for i in range(pos+1,len(y)):
                syl.append(y[i])

            if len(syl) == 0:
                syl=list(y)

            last_syl_a.append(syl)

        print(last_syl_a)

        for y in b:
            syl = []
            pos = 0
            for i in range(0,len(y)):
                if(not y[i][-1].isdigit()):
                    pos = i
                    break
            for i in range(pos+1,len(y)):
                syl.append(y[i])

            if len(syl) == 0:
                syl=list(y)

            last_syl_b.append(syl)

        print(last_syl_b)

        if any(i in last_syl_a for i in last_syl_b):
            print "Rhyming - Yes "
            return True

        else:
            print "Suffix Procedure"
            if len(last_syl_a[0]) > len(last_syl_b[0]):
                big = last_syl_a
                small = last_syl_b
            else:
                big = last_syl_b
                small = last_syl_a

            for i in big:
                for j in small:
                    count = 0
                    for k in range(0,len(j)):
                        if j[-(k+1)] == i[len(i)-(k+1)]:
                            count = count + 1
                    if count == len(j) and count > 0:
                        print "Rhyming - yes", i,j
                        return True

            return False
    else:
        return False

def rhyme(a,b ):
    a = a.lower()
    b = b.lower()
    # print "----------------------------------"
    print "Rhyming ", a, b
    D = Dictionary()
    if a in D.keys() and b in D.keys():
        a = D[a]
        print a
        b = D[b]
        print b

        last_syl_a = []
        last_syl_b = []

        # for each pronunciation of the word
        for y in a:
            syl = []
            pos = 0
            for i in range(0, len(y)):
                if y[i][-1].isdigit():
                    pos = i
                    break
            for i in range(pos, len(y)):
                syl.append(y[i])

            last_syl_a.append(syl)
        print(last_syl_a)

        for y in b:
            syl = []
            pos = 0
            for i in range(0, len(y)):
                if y[i][-1].isdigit():
                    pos = i
                    break
            for i in range(pos, len(y)):
                syl.append(y[i])

            last_syl_b.append(syl)
        print(last_syl_b)

        if any(i in last_syl_a for i in last_syl_b):
            print "Rhyming - Yes "
            return True
        else:
            print "Suffix Procedure"
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
                        if j[-(k + 1)] == i[len(i) - (k + 1)]:
                            count = count + 1
                    if count == len(j) and count > 0:
                        print "Rhyming - yes", i, j
                        return True

            return False
    else:
        return False

def guess_syllables(word):

    # Guess the number of syllables in a word that may not be present in the CMU dictionary
    D = nltk.corpus.cmudict.dict()

    word = word.lower().strip(".:;?!")
    if word in D.keys():
        print "Word present in CMU Dictionary"
        return num_syl(word)

    word = word.lower()
    print(word)

    # Count the syllables in the word.
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

def main():
    a = """Writing a Limerick's absurd,
Line one and line five rhyme in word,
And just as you've reckoned
They rhyme with the second;
The fourth line must rhyme with the third.
    """

    b="""There was a young man so benighted
He never knew when he was slighted;
He would go to a party
And eat just as hearty,
As if he'd been really invited."""

    c = """There was an Old Man with a nose,
Who said, 'If you choose to suppose,
That my nose is too long,
You are certainly wrong!'
That remarkable Man with a nose."""


    print limerick(a)


if __name__ == '__main__':
    main()

