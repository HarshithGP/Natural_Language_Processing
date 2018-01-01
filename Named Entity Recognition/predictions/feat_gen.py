#!/bin/python

import argparse
import sys
import os.path
import re
import pandas as pd
from nltk.corpus import stopwords


# company features
company = set((pd.read_csv('data/lexicon/business.consumer_company', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
sponser = set((pd.read_csv('data/lexicon/business.sponsor', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
venture = set((pd.read_csv('data/lexicon/venture_capital.venture_funded_company', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


# location features 
#location = set((pd.read_csv('data/lexicon/location', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


country = set((pd.read_csv('data/lexicon/location.country', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
venues = set((pd.read_csv('data/lexicon/venues', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())

# person features
person = set((pd.read_csv('data/lexicon/people.person', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
lastname = set((pd.read_csv('data/lexicon/lastname.5000', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
firstname = set((pd.read_csv('data/lexicon/firstname.1000', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())

familyname = set((pd.read_csv('data/lexicon/people.family_name', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
#sports
sports_team = set((pd.read_csv('data/lexicon/sports.sports_team', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
sports_league = set((pd.read_csv('data/lexicon/sports.sports_league', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())

#tv programs
tv_prog = set((pd.read_csv('data/lexicon/tv.tv_program', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
tv_net = set((pd.read_csv('data/lexicon/tv.tv_network', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


movie = set((pd.read_csv('data/lexicon/movie.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
music = set((pd.read_csv('data/lexicon/music.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())

education = set((pd.read_csv('data/lexicon/education.university', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
#product
product = set((pd.read_csv('data/lexicon/product', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
consumer_product = set((pd.read_csv('data/lexicon/business.consumer_product', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


# features for links
#links = set((pd.read_csv('data/lexicon/links.txt', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


event = set((pd.read_csv('data/lexicon/time.recurring_event', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
government = set((pd.read_csv('data/lexicon/government.government_agency', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
road = set((pd.read_csv('data/lexicon/transportation.road', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
business = set((pd.read_csv('data/lexicon/business.sponsor', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
game = set((pd.read_csv('data/lexicon/cvg.computer_videogame', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
developer= set((pd.read_csv('data/lexicon/cvg.cvg_developer', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
museum = set((pd.read_csv('data/lexicon/architecture.museum', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
vehicle = set((pd.read_csv('data/lexicon/automotive.make', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
model= set((pd.read_csv('data/lexicon/automotive.model', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
award = set((pd.read_csv('data/lexicon/award.award', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())

#bigdict = set((pd.read_csv('data/lexicon/bigdict', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())


"""
CompanyH = set((pd.read_csv('data/H_Lex/company.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
NamesH = set((pd.read_csv('data/H_Lex/names.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
LocationH = set((pd.read_csv('data/H_Lex/location.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
ProductH = set((pd.read_csv('data/H_Lex/product.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
SportsH = set((pd.read_csv('data/H_Lex/sports.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
TVH = set((pd.read_csv('data/H_Lex/tv.lex', header=None, delimiter = '\n', quoting = 3, encoding='utf-8'))[0].tolist())
"""

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    pass



def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """

    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")
   
    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    #ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")

    #word = re.sub('[^a-zA-Z0-9\n ]', '', word)
    """
    if word in CompanyH:
        ftrs.append("IS_COMPANY")
    if word in NamesH:
        ftrs.append("IS_NAMES")
        
    if word in LocationH:
        ftrs.append("IS_LOC")

    if word in ProductH:
        ftrs.append("IS_PROD")
    if word in SportsH:
        ftrs.append("IS_SPORTS")
    if word in TVH:
        ftrs.append("IS_TV")

    """

    """
    if word in company:
        ftrs.append("IS_COMPANY")
    if word in sponser:
        ftrs.append("IS_SPONSER")
    if word in venture:
        ftrs.append("IS_VENTURE")
    """

    #if word in location:
        #ftrs.append("IS_LOC")
    """    
    if word in country:
        ftrs.append("IS_COUNTRY")
    if word in venues:
        ftrs.append("IS_VENUES")


    if word in person:
        ftrs.append("IS_PERSON")

    if word in lastname:
        ftrs.append("IS_LASTNAME")
    if word in firstname:
        ftrs.append("IS_FIRSTNAME")
    if word in familyname:
        ftrs.append("IS_FAMILYNAME")

    if word in sports_team:
        ftrs.append("IS_SPORTSTEAM")
    if word in sports_league:
        ftrs.append("IS_SPORTSLEAGUE")
    
    if word in tv_prog:
        ftrs.append("IS_TVProg")
    if word in tv_net:
        ftrs.append("IS_TVNet")

    if word in product:
        ftrs.append("IS_PRODUCT")
    if word in consumer_product:
        ftrs.append("IS_CONS_PRODUCT")
    if word in education:
        ftrs.append("IS_EDU")

    if word in movie:
        ftrs.append("IS_MOVIE")
    if word in music:
        ftrs.append("IS_MUSIC")

    if word in government:
        ftrs.append("IS_GOVRN")
    if word in event:
        ftrs.append("IS_EVENT")
    if word in road:
        ftrs.append("IS_ROAD")
    #if word in internet:
        #ftrs.append("IS_INTERNET")
    if word in business:
        ftrs.append("IS_BUSINESS")
    if word in game:
        ftrs.append("IS_GAME")
    if word in developer:
        ftrs.append("IS_DEVLOPER")
    if word in museum:
        ftrs.append("IS_MUSEUM")
    if word in vehicle:
        ftrs.append("IS_VEHICLE")
    if word in model:
        ftrs.append("IS_MODEL")
    if word in award:
        ftrs.append("IS_AWARD")
    

    
    if word in bigdict:
        ftrs.append("IS_BIGDICT")
    """
    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I","like","#to","Play","football","in","the","rain","in","India@" ],
    [ "I","#to","Play","football1","rain","in","India@" ],
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
            print('\n')


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    