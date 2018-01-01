# Named Entity Recognition

Project description
- Performed supervised named entity recognition for Twitter data. The NER dataset contains tweets annotated with their named entities in the BIO format (Beginning of an entity, Inside an entity or Outside of entities).
- Used two sequence taggers - logistic regression and CRF. Both taggers use the features generated for each token. The dynamic Viterbi algorithm is implemented and used for decoding.
- Additional features are generated for each token to enhance the accuracy of the taggers.
- Evaluation metrics of precision, recall and F-measure as well as the CONLL evaluation script are used to compare the relative performances of the two taggers and draw insightful conclusions.
