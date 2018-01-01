# Feature Engineering for Author Identification

Project description
- Implemented the Naive Bayes Classifier using python's nltk library to identify the author of written content.
- The classifier was trained using the bag of words model comprising of the frequency of distinct words which resulted in a baseline accuracy of 77% on the development data comprising of textual content extracted from the written works authored by William Shakespeare and Emily Bronte.
- Enhanced the accuracy of the model to achieve an accuracy of 98.6% on the development data and 94.67% on the test data through feature engineering techniques.
- Features used: Word stemming using the snowball stemmer, removal of common stopwords, bigram and trigram count, average sentence length, text normalization, part of speech tagging and CMU's dictionary of word pronunciations.
