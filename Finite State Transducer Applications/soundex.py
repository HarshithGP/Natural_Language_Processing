"""
CSCI 544 - Natural Language Processing
University of Southern California,
Fall 2017

HomeWork Assignment 2
Code developed by - HARSHITH GURU PRASAD
CS GRADUATE STUDENT, USC VITERBI
"""

from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # first FST definition
    f1 = FST('soundex-generate')

    f1.add_state('start')
    f1.initial_state = 'start'

    #terminal states
    states = ['0', '1', '2', '3', '4', '5', '6']
    for state in states:
        f1.add_state(state)
        f1.set_final(state)

    state_0 = ['a', 'e', 'i', 'o', 'u', 'h', 'w', 'y', 'A', 'E', 'I', 'O', 'U', 'H', 'W', 'Y']
    state_1 = ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']
    state_2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']
    state_3 = ['d', 't', 'D', 'T']
    state_4 = ['l', 'L']
    state_5 = ['m', 'n', 'M', 'N']
    state_6 = ['r', 'R']
    digits = ['0','1','2','3','4','5','6','7','8','9']

    """
        0 - a, e, i, o, u, h, w, y
        1 - b, f, p ,v
        2 - c, g, j, k, q, s, x, z
        3 - d, t
        4 - l
        5 - m, n
        6 - r 

    """

    # initial transition from start state to the respective final state
    for letter in string.ascii_letters:
        if letter in state_0:
            f1.add_arc('start', '0', (letter), (letter))
        if letter in state_1:
            f1.add_arc('start', '1', (letter), (letter))
        if letter in state_2:
            f1.add_arc('start', '2', (letter), (letter))
        if letter in state_3:
            f1.add_arc('start', '3', (letter), (letter))
        if letter in state_4:
            f1.add_arc('start', '4', (letter), (letter))
        if letter in state_5:
            f1.add_arc('start', '5', (letter), (letter))
        if letter in state_6:
            f1.add_arc('start', '6', (letter), (letter))

    # from all states, make a transition to state 0 without appending any number - deletes vowels
    for state in states:
        for letter in state_0:
            f1.add_arc(state, '0', (letter), ())

    # remain in same state without replacing the letter with a no if the letter is in the same number group
    for letter in state_1:
        f1.add_arc('1', '1', (letter), ())
    for letter in state_2:
        f1.add_arc('2', '2', (letter), ())
    for letter in state_3:
        f1.add_arc('3', '3', (letter), ())
    for letter in state_4:
        f1.add_arc('4', '4', (letter), ())
    for letter in state_5:
        f1.add_arc('5', '5', (letter), ())
    for letter in state_6:
        f1.add_arc('6', '6', (letter), ())

    # arcs for replacing letters with their corresponding number group no

    for state in states:

        if state != '1':
            for i in state_1:
                f1.add_arc(state, '1', (i), ('1'))

        if state != '2':
            for i in state_2:
                f1.add_arc(state, '2', (i), ('2'))

        if state != '3':
            for i in state_3:
                f1.add_arc(state, '3', (i), ('3'))

        if state != '4':
            for i in state_4:
                f1.add_arc(state, '4', (i), ('4'))

        if state != '5':
            for i in state_5:
                f1.add_arc(state, '5', (i), ('5'))

        if state != '6':
            for i in state_6:
                f1.add_arc(state, '6', (i), ('6'))

    f1.add_state('num')
    f1.set_final('num')
    for digit in digits:
        f1.add_arc('start','num',(digit),(digit))
        f1.add_arc('num','num',(digit),(digit))

    return f1

def truncate_to_three_digits():
    """
    A FST that will truncate a soundex string to three digits
    """
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('start')
    f2.add_state('d1')
    f2.add_state('d2')
    f2.add_state('d3')
    f2.add_state('end')
    f2.initial_state = 'start'
    f2.set_final('end')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('start', 'd1', (letter), (letter))

    f2.add_arc('d1', 'end', (),())
    f2.add_arc('d2', 'end', (),())
    f2.add_arc('d3', 'end', (),())

    for n in range(10):
        f2.add_arc('d1', 'd2', (str(n)), (str(n)))
        f2.add_arc('d2', 'd3', (str(n)), (str(n)))
        f2.add_arc('d3', 'end', (str(n)), (str(n)))
        f2.add_arc('end', 'end', (str(n)), ())

    digits = ['0','1','2','3','4','5','6','7','8','9']
    for digit in digits:
        f2.add_arc('start','d2',(digit),(digit))

    return f2

def add_zero_padding():
    # Third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('start')
    f3.add_state('p1')
    f3.add_state('p2')
    f3.add_state('p3')
    f3.add_state('end')

    f3.initial_state = 'start'
    f3.set_final('end')

    f3.add_arc('start','p1',(),())
    for letter in string.letters:
        f3.add_arc('start', 'p1', (letter), (letter))

    f3.add_arc('p1', 'p2', (), ('0'))
    f3.add_arc('p2', 'p3', (), ('0'))
    f3.add_arc('p3', 'end', (), ('0'))

    for number in xrange(10):
        f3.add_arc('p1', 'p2', (str(number)), (str(number)))
        f3.add_arc('p2', 'p3', (str(number)), (str(number)))
        f3.add_arc('p3', 'end', (str(number)), (str(number)))

    return f3

if __name__ == '__main__':
    #print "Enter a Name"
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))

    print "------------ Tracing --------------------"
    print "---------STEP 1-------------"
    print trace(f1, user_input)
    step1 = composechars(tuple(user_input), f1)
    print step1

    print "----------STEP 2------------"
    print trace(f2, step1)
    step2 = composechars(tuple(step1), f2)
    print step2

    print "----------STEP 3------------"
    print trace(f3, step2)
    step3 = composechars(tuple(step2),f3)
    print step3



