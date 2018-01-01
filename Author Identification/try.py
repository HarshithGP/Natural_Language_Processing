
from nltk import ngrams
sentence = 'this is a foo bar sentences and i want to ngramize it'

bigrams = ngrams(sentence.split(), 2)
for grams in bigrams:
  print grams
