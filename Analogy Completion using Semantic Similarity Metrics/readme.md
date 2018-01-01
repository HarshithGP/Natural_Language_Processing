# Analogy Completion using Semantic Similarity Metrics

Project description
- Implemented comparison functions for word representations and used the functions
and representations to solve semantic similarity tasks.
- Similarity metrics used - Cosine similarity using context count vectors and dense vector embeddings for a list of 4000 words.
- Semantic scores determined using the cosine similarity metric helped identify the words that are closest in meaning to a given query word.
- Mathematical operations helped deduce the missing words that completed the analogy
eg ( man : king :: woman : ? ) returns queen as the missing word
- Attempted to enhance the accuracy using alternate metrics such as Jaccard and Dice similarity.
- Used pre trained word vectors from https://nlp.stanford.edu/projects/glove/. Downloaded the vectors for words from Wikipedia 2014 and Gigaword5(822 MB).
- Tried to add the context of word stem for word vectors. Logic: words having the same stem are more likely to have the same semantic meaning.
