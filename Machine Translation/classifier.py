
# Natural Language Processing

# Importing the libraries
import numpy as np

import pandas as pd
import re
# Importing the dataset
dataset = pd.read_csv('data/hyp1-hyp2-ref', delimiter = '\n', quoting = 3)
dataset = dataset[0:10000]
labels = pd.read_csv('data/dev.answers', delimiter='\n')
labels = labels[0:10000]

corpus = []
sentences = []
sentences = dataset.values.tolist()
for sentence in sentences:
    word = sentence[0].lower()
    word = re.sub('[^a-zA-Z0-9]',' ', word)
    #word = word.split()
    corpus.append(word)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()

"""
# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size = 0, random_state = 0)
"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X, labels)
#classifier.fit(X_train, y_train)

"""
y_pred = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
for y in y_pred:
	print(y)
"""
y_pred = classifier.predict(X)
f = open('eval_h.txt', 'w')
for y in y_pred:
	f.write(str(y))
	f.write('\n')
