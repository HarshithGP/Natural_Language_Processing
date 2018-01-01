"""
CSCI 544 - Natural Language Processing
University of Southern California,
Fall 2017

HomeWork Assignment 2
Code developed by - HARSHITH GURU PRASAD
CS GRADUATE STUDENT, USC VITERBI
"""

import sys
from fst import FST
from fsmutils import composewords, trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = "et"

def prepare_input(integer):

    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'

    #terminal states
    single_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    #Intermediate States
    double_digits = ['1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a']
    triple_digits = ['1aa', '2aa', '3aa', '4aa', '5aa', '6aa', '7aa', '8aa', '9aa']

    i = 0
    for state in single_digits:
        f.add_state(state)
        f.set_final(state)
        f.add_arc('start', state, [str(i)], [kFRENCH_TRANS[i]])
        f.add_arc(state, state, [], [])
        i = i+1

    #To eliminate zeroes before the most significant digit
    f.add_arc('start', 'start', ['0'], [])

    #all 2 digit numbers starting with 1 ie 10 - 19
    f.add_state('1a')
    f.add_arc('start', '1a', ['1'],[])
    i = 0
    for state in single_digits[0:7]:
        f.add_arc('1a', state, [str(i)], [kFRENCH_TRANS[i+10]])
        i = i+1

    f.add_arc('1a', '7', [str(7)], [ kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[7] ])
    f.add_arc('1a', '8', [str(8)], [ kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[8] ])
    f.add_arc('1a', '9', [str(9)], [ kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[9] ])

    #all 2 digit nos starting with 2 ie 20 - 29
    f.add_state('2a')
    f.add_arc('start', '2a', ['2'], [])
    f.add_arc('2a', '0', [str(0)], [kFRENCH_TRANS[20]])
    f.add_arc('2a', '1', [str(1)], [kFRENCH_TRANS[20] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
    i = 2
    for state in single_digits[2:10]:
        f.add_arc('2a', state, [str(i)], [kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    #all 2 digit nos starting with 3 ie 30 - 39
    f.add_state('3a')
    f.add_arc('start', '3a', ['3'], [])
    f.add_arc('3a', '0', [str(0)], [kFRENCH_TRANS[30]])
    f.add_arc('3a', '1', [str(1)], [kFRENCH_TRANS[30] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
    i = 2
    for state in single_digits[2:10]:
        f.add_arc('3a', state, [str(i)], [kFRENCH_TRANS[30] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # all 2 digit nos starting with 4 ie 40 - 49
    f.add_state('4a')
    f.add_arc('start', '4a', ['4'], [])
    f.add_arc('4a', '0', [str(0)], [kFRENCH_TRANS[40]])
    f.add_arc('4a', '1', [str(1)], [kFRENCH_TRANS[40] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
    i = 2
    for state in single_digits[2:10]:
        f.add_arc('4a', state, [str(i)], [kFRENCH_TRANS[40] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # all 2 digit nos starting with 5 ie 50 - 59
    f.add_state('5a')
    f.add_arc('start', '5a', ['5'], [])
    f.add_arc('5a', '0', [str(0)], [kFRENCH_TRANS[50]])
    f.add_arc('5a', '1', [str(1)], [kFRENCH_TRANS[50] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
    i = 2
    for state in single_digits[2:10]:
        f.add_arc('5a', state, [str(i)], [kFRENCH_TRANS[50] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # all 2 digit nos starting with 6 ie 60 - 69
    f.add_state('6a')
    f.add_arc('start', '6a', ['6'], [])
    f.add_arc('6a', '0', [str(0)], [kFRENCH_TRANS[60]])
    f.add_arc('6a', '1', [str(1)], [kFRENCH_TRANS[60] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[1]])
    i = 2
    for state in single_digits[2:10]:
        f.add_arc('6a', state, [str(i)], [kFRENCH_TRANS[60] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    #all 2 digit nos starting with 7 ie 70 - 79
    f.add_state('7a')
    f.add_arc('start', '7a', ['7'], [])
    f.add_arc('7a', '0', [str(0)], [ kFRENCH_TRANS[60] + " " + kFRENCH_TRANS[10] ])
    f.add_arc('7a', '1', [str(1)], [kFRENCH_TRANS[60] + " " + kFRENCH_AND + " " + kFRENCH_TRANS[11]])
    i = 2
    for state in single_digits[2:10]:
        if i < 7:
            f.add_arc('7a', state, [str(i)], [kFRENCH_TRANS[60] + " " + kFRENCH_TRANS[i+10]])
        else:
            f.add_arc('7a', state, [str(i)], [kFRENCH_TRANS[60] + " " + kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # all 2 digit nos starting with 8 ie 80 - 89
    f.add_state('8a')
    f.add_arc('start', '8a', ['8'], [])
    f.add_arc('8a', '0', [str(0)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    i = 1
    for state in single_digits[1:10]:
        f.add_arc('8a', state, [str(i)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # all 2 digit nos starting with 9 ie 90 - 99
    f.add_state('9a')
    f.add_arc('start', '9a', ['9'], [])
    f.add_arc('9a', '0', [str(0)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[10]])
    i = 1
    for state in single_digits[1:10]:
        if i < 7:
            f.add_arc('9a', state, [str(i)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[10+i]])
        else:
            f.add_arc('9a', state, [str(i)], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20] + " " + kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[i]])
        i = i + 1

    # ----------------------------- 3 DIGIT NUMBERS ---------------------------

    f.add_state('t')
    #temp state

    for state in triple_digits:
        f.add_state(state)

    j = 1
    for state in triple_digits:

        if j == 1:
            f.add_arc('start', state, [str(j)], [kFRENCH_TRANS[100]])
        else:
            f.add_arc('start', state, [str(j)], [kFRENCH_TRANS[j] + " " + kFRENCH_TRANS[100]])

        f.add_arc(state, 't', [str(0)], [])
        f.add_arc('t', '0', [str(0)], [])

        i = 1
        for s in single_digits[1:10]:
            f.add_arc('t', s, [str(i)], [kFRENCH_TRANS[i]])
            i = i + 1

        i = 1
        for s in double_digits:
            f.add_arc(state, s, [str(i)], [])
            i = i + 1

        j = j+1

    return f

if __name__ == '__main__':
    #print "Enter input"
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print prepare_input(user_input)
        #print trace(f, str(user_input))
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
        #print composewords(str(user_input),f)